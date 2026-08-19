# Data Reconcilier

Pipeline em Python para conciliar e validar produtos entre o banco de dados interno (**EMPRESA / Oracle**) e o catálogo do ERP **MICROVIX** (~500 mil produtos).

O objetivo é identificar quais produtos — vindos de **Planilhas de Coleção de Modelos**, **Planilhas de Divergências (EANs)** ou **Notas Fiscais XML (DANFE/NFe)** — ainda **não existem** na base da Microvix, e gerar um Excel (`.xlsx`) no layout exato aceito pela importação nativa do ERP.

> 📖 Para o racional completo de arquitetura e decisões de design, veja [`docs/context.md`](docs/context.md).  
> 🗺️ Para o status detalhado de cada etapa, veja [`docs/roadmap_pipeline_microvix.md`](docs/roadmap_pipeline_microvix.md).

---

## Arquitetura em uma frase

`entrypoints` orquestra, `core` decide (funções puras e regras de negócio), `infra` conversa com o mundo externo (Oracle, arquivos de log, variáveis de ambiente). Nenhum módulo de `core` depende de Typer, Oracle ou sistema de arquivos diretamente.

```
Planilha / EAN / XML NFe ──▶ core/parser.py ──▶ core/empresa_repo.py (Oracle)
                                                        │
                                                        ▼
                                             core/divergencia.py (limpo x divergente)
                                                        │
                                                        ▼
                                                 core/dedupe.py
                                                        │
                                                        ▼
                                     core/diff.py  ◀── core/mirror_sync.py (espelho Microvix)
                                                        │
                                                        ▼
                                           results/*.xlsx (pronto pra importar)
```

---

## Pré-requisitos

- **Python 3.12+**
- [uv](https://docs.astral.sh/uv/) como gerenciador de pacotes/ambiente
- Oracle Instant Client (Basic Light) instalado localmente, para conexão em **modo Thick**
- Acesso de leitura ao banco Oracle da EMPRESA
- Um export `.xlsx` atualizado do catálogo Microvix (usado como espelho local de alta performance)

---

## Instalação

```bash
git clone <repo>
cd data-reconcilier
uv sync
```

## Configuração

Copie `.env.example` para `.env` e preencha as credenciais:

```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_SERVICE=nome_do_servico
ORACLE_CLIENT_LIB_DIR=/caminho/para/instantclient
```

---

## Uso da CLI

O ponto de entrada oficial é o [`main.py`](main.py), desenvolvido com [Typer](https://typer.tiangolo.com/).

### 1. Fluxo de coleção (busca no Oracle por modelo)

```bash
python main.py colecao \
  -n minha_colecao \
  -p data/modelos.xlsx \
  -b data/microvix_espelho.xlsx
```

**Saídas geradas:**
- `results/<nome>_<timestamp>_não_cadastrados.xlsx` — produtos novos prontos para importação no ERP.
- `results/check/<nome>_<timestamp>_a_verificar.xlsx` — itens com divergência cadastral para revisão manual.

---

### 2. Fluxo de divergentes (conciliação direta por EAN)

Utilizado para revalidar a planilha `a_verificar.xlsx` diretamente contra o espelho Microvix após correções:

```bash
python main.py divergentes \
  -n minha_verificacao \
  -p results/check/a_verificar.xlsx \
  -b data/microvix_espelho.xlsx
```

---

### 3. Fluxo de Nota Fiscal (XML da NFe)

Extrai os EANs do XML da NF-e, consulta o Oracle e faz o diff contra a Microvix:

```bash
python main.py nfe \
  -n minha_nota \
  -x data/nota_fiscal.xml \
  -b data/microvix_espelho.xlsx
```

> 💡 *Cada execução gera automaticamente um arquivo de log com timestamp na pasta `logs/`.*

---

## Testes Automatizados

O projeto possui suíte de testes unitários e de integração com pytest:

```bash
uv run pytest
# ou
pytest
```

---

## Estrutura de Pastas

```
core/           # Regras de negócio puras (parser, diff, dedupe, divergência, repo Oracle)
entrypoints/    # Orquestração desacoplada dos fluxos (colecao, divergentes, nfe)
infra/          # Infraestrutura (conexão Oracle Thick, logging, .env, SQL loader)
sql/            # Queries Oracle (busca_por_modelo.sql e busca_por_ean.sql)
tests/          # Suíte de testes unitários e de CLI com pytest
results/        # Planilhas de saída prontas para importação (não versionado)
  └── check/    # Planilhas de itens retidos para conferência manual
logs/           # Arquivos de log de execução detalhados (não versionado)
docs/           # Documentação arquitetural (context.md) e roadmap
main.py         # Interface CLI oficial com Typer
```

---

## Status do Projeto

| Fase | Descrição | Status |
|---|---|:---:|
| **0** | Setup do projeto (pastas, dependências, Oracle Thick, pytest) | ✅ Concluído |
| **1** | Núcleo de negócio puro e desacoplado (`core/`) | ✅ Concluído |
| **2** | Mirror stub em memória com Polars (leitura em milissegundos) | ✅ Concluído |
| **3** | Orquestração dos 3 fluxos (`colecao`, `divergentes`, `nfe`) e CLI Typer | ✅ Concluído |
| **4** | Validação operacional com dados reais em produção | ✅ Concluído |
| **5** | Decisão Técnica: Espelho local consolidado para execuções instantâneas | ✅ Concluído |

---

## Diretrizes de Desenvolvimento

- Manter funções em `core/` puras (sem I/O ou dependência de framework), com tipagem estrita.
- Novas consultas Oracle devem residir em `sql/` e ser carregadas via `infra/sql_loader.py`.
- Qualquer nova funcionalidade deve ser acompanhada de testes em `tests/` e documentada em `docs/context.md`.