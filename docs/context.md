# Contexto e Arquitetura do Projeto — Data Reconcilier (Pipeline Microvix)

## 1. Visão Geral do Projeto

O **Data Reconcilier** é um pipeline em Python desenvolvido para conciliar e validar produtos entre o banco de dados interno (**EMPRESA / Oracle**) e o catálogo do ERP da **MICROVIX** (~500 mil produtos).

O objetivo principal é identificar quais produtos (seja vindos de **Planilhas de Coleção de Modelos**, **Arquivos de Divergências/EANs** ou **Notas Fiscais XML**) ainda **não existem** na base da Microvix e gerar um arquivo Excel (`.xlsx`) no layout exato aceito pela importação nativa do ERP.

---

## 2. Pilares de Arquitetura e Decisões de Design

### 2.1 Princípio da Responsabilidade Única (SRP) e Desacoplamento
Toda a lógica de negócio reside no pacote `core/` como funções puras ou repositórios específicos. Nenhum módulo do `core/` ou `entrypoints/` depende de interfaces de usuário (CLI, Typer, Flask, etc.).

- **`core/parser.py`**: Responsável **exclusivamente** por abrir arquivos de entrada, extrair identificadores de interesse (`extrair_modelos_planilha`, `extrair_eans_planilha` e `extrair_eans_xml`), sanitizar (`.drop_nulls()`, `.str.strip_chars()`, `.unique()`) e retornar listas limpas de strings (`list[str]`).
- **`core/empresa_repo.py`**: Responsável por consultar a base Oracle em lotes (`batched(900)`), injetando a conexão recebida por parâmetro. Implementa `buscar_por_modelo` (usando `busca_por_modelo.sql`) e `buscar_por_ean` (usando `busca_por_ean.sql`), tratando comparações `CHAR` vs `VARCHAR2` via `TRIM`.
- **`core/divergencia.py`**: Particiona os dados em **limpos** (seguem o fluxo) e **retidos** (divergências de cadastro em colunas além de `"Coleção"` para revisão manual).
- **`core/dedupe.py`**: Remove duplicidades exatas por EAN (`"Código"`).
- **`core/diff.py`**: Executa a filtragem de candidatos ainda não existentes na Microvix via `filter` + `is_in`, comparando `candidatos["Código"]` contra a **união** de `mirror["Código"]` e `mirror["Código de barras"]` (`pl.concat([...]).drop_nulls().unique()`).
- **`core/build_import.py`**: Helper enxuto de exportação final para o layout Microvix.
- **`core/mirror_sync.py`**: Carrega o espelho da Microvix (stub via Excel em memória usando `calamine` e `schema_overrides={"Código": pl.String, "Código de barras": pl.String}`).

### 2.2 Camada de Entrada e CLI (`entrypoints/` e `main.py`)
- **`entrypoints/fluxo_colecao.py`**: Orquestrador do fluxo por modelo (Leitura de Planilha ➔ Busca Oracle ➔ Divergências ➔ Dedupe ➔ Diff ➔ Exportação de `não_cadastrados.xlsx` e `a_verificar.xlsx`).
- **`entrypoints/fluxo_divergentes.py`**: Orquestrador do fluxo direto de conciliação de EANs a verificar contra o espelho Microvix.
- **`entrypoints/fluxo_nfe.py`**: Orquestrador do fluxo a partir de XML de Nota Fiscal (Parse XML ➔ Busca Oracle EAN ➔ Divergências ➔ Dedupe ➔ Diff ➔ Exportação).
- **`main.py` (CLI Central)**: Ponto de entrada oficial construído com **Typer**. Expõe subcomandos (`colecao`, `divergentes` e `nfe`), opções (`-n`, `-p`, `-b`, `-x`), inicializa `setup_logging` e delega a execução aos fluxos desacoplados.

### 2.3 Infraestrutura e Logging
- **`infra/log_config.py`**: Configuração centralizada de logs com rotação/criação automática da pasta `logs/`, handlers para console (`sys.stdout`) e arquivo físico com timestamp (`UTF-8`).
- **`infra/oracle.py`**: Gerenciamento de conexões Oracle em modo Thick com context manager `@contextmanager get_connection()`.
- **`infra/sql_loader.py`**: Carregamento dinâmico dos arquivos SQL.

---

## 3. Stack Tecnológica

| Componente | Tecnologia | Observação |
|---|---|---|
| Linguagem | Python 3.10+ | Padrão do projeto |
| Engine de DataFrame | **Polars** | Utilizado em todo o projeto para leitura de Excel e operações relacionais |
| CLI Framework | **Typer** | Interface de linha de comando com subcomandos (`main.py`) |
| Conexão Banco | **python-oracledb (Modo Thick)** | Requer Oracle Instant Client Basic Light configurado via `ORACLE_CLIENT_LIB_DIR` no `.env` |
| Leitura de Excel | **Calamine** (`engine="calamine"`) | Motor de alta performance para Polars |
| Exportação de Excel | **XlsxWriter** | Utilizado pelo `write_excel` do Polars |

---

## 4. Estrutura de Pastas

```
data_reconcilier/
├── core/
│   ├── parser.py            # Extração e higienização de modelos, EANs e XMLs de NFe
│   ├── empresa_repo.py      # Queries Oracle em lote (EAN e Modelo)
│   ├── divergencia.py       # Identificação de divergências de cadastro (limpo, retido)
│   ├── dedupe.py            # Deduplicação por EAN ("Código")
│   ├── diff.py              # Anti-join / diff contra o espelho Microvix
│   ├── mirror_sync.py       # Leitura do espelho Microvix (stub XLSX)
│   └── build_import.py      # Exportação para o layout XLSX da Microvix
├── docs/
│   ├── context.md           # Visão geral e decisões de arquitetura (este arquivo)
│   └── roadmap_pipeline_microvix.md  # Roadmap detalhado das fases de desenvolvimento
├── entrypoints/
│   ├── fluxo_colecao.py     # Orquestração do fluxo de coleções
│   ├── fluxo_divergentes.py # Orquestração da conciliação direta de divergentes
│   └── fluxo_nfe.py         # Orquestração do fluxo de NFe XML
├── infra/
│   ├── config.py            # Leitura do .env
│   ├── log_config.py        # Configuração central de logging (console e arquivo)
│   ├── oracle.py            # Gerenciamento de conexão Oracle (Thick Mode)
│   └── sql_loader.py        # Carregador de scripts SQL
├── logs/                    # Logs de execução com timestamp (criados automaticamente)
├── results/                 # Planilhas de saída geradas pelo pipeline
│   └── check/               # Planilhas de itens retidos para revisão manual (a_verificar)
├── sql/
│   ├── busca_por_modelo.sql # Query Oracle para expansão de modelo em EANs
│   └── busca_por_ean.sql    # Query Oracle para busca direta por EAN
├── tests/                   # Suíte de testes unitários e de integração (pytest)
├── main.py                  # Ponto de entrada oficial Typer (subcomandos: colecao, divergentes, nfe)
├── .env.example
└── pyproject.toml
```

---

## 5. Diretrizes de Desenvolvimento para IAs / Mentores
- **Modo Mentor**: Não gerar blocos de código completos automaticamente nas respostas, exceto quando explicitamente solicitado pelo usuário. Estimular o raciocínio lógico, arquitetural e a autonomia do desenvolvedor.
- **Código Limpo & SRP**: Manter funções puras no `core/` e `entrypoints/`, garantir tipagem e injeção de dependências.
