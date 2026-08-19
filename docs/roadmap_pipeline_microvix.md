# Roadmap — Pipeline de validação MICROVIX x EMPRESA

## Contexto rápido

Três entradas (planilha de modelos de coleção, planilha de divergências e nota fiscal XML) convergem para um núcleo
compartilhado que compara candidatos contra um espelho local do catálogo MICROVIX (~500 mil
produtos, Polars em memória, sincronizado sob demanda) e gera planilhas XLSX prontas para importação no ERP ou revisão manual.

Stack: Python 3.10+, Typer (CLI em `main.py`), Polars (DataFrame único do projeto), python-oracledb em **modo Thick** (leitura na base EMPRESA — Instant Client necessário), Calamine (leitura de Excel) e XlsxWriter.

## Legenda de prioridade

- 🔴 **P0** — bloqueador. Nada essencial funciona sem isso.
- 🟡 **P1** — importante para o pipeline ser usável de ponta a ponta.
- 🟢 **P2** — importante, mas não bloqueia o uso real; pode vir depois.
- 🔵 **P3** — backlog / futuro. Não fazer agora.

---

## Fase 0 — Setup do projeto (100% CONCLUÍDA)

- [x] 🔴 **0.1** Criar estrutura de pastas (`core/`, `entrypoints/`, `infra/`, `tests/`, `main.py`)
- [x] 🔴 **0.2** Configurar dependências no `pyproject.toml` (typer, polars, python-calamine, xlsxwriter, python-oracledb, python-dotenv, pytest)
- [x] 🔴 **0.3** Criar `.env.example` com as variáveis de conexão Oracle
- [x] 🔴 **0.3.1** Instalação do Oracle Instant Client Basic Light
- [x] 🔴 **0.3.2** Configuração do `ORACLE_CLIENT_LIB_DIR` no `.env` e inicialização no `infra/oracle.py`
- [x] 🟡 **0.4** Teste de conexão Oracle em modo Thick validado com sucesso
- [x] 🟢 **0.5** Configurar `pytest` básico e teste de fumaça (smoke test)

---

## Fase 1 — Núcleo que NÃO depende do mirror_sync (100% CONCLUÍDA)

- [x] 🔴 **1.0a** `infra/config.py` — leitura do `.env` via `pydantic-settings`
- [x] 🔴 **1.0b** `infra/oracle.py` — gerenciador de conexões Oracle (Thick Mode) via context manager
- [x] 🔴 **1.0c** `infra/log_config.py` — setup centralizado de logging com handlers para console e arquivo com timestamp em `logs/`
- [x] 🔴 **1.0d** `infra/sql_loader.py` — carregamento dinâmico de `busca_por_modelo.sql` e `busca_por_ean.sql`
- [x] 🔴 **1.1a** `core/empresa_repo.py` (`buscar_por_modelo`) — busca no Oracle em lotes de 900 com batching e conversão para Polars
- [x] 🔴 **1.1b** `core/empresa_repo.py` (`buscar_por_ean`) — busca direta por EAN no Oracle para conciliação direta
- [x] 🔴 **1.2a** `core/divergencia.py` — partição entre produtos limpos e divergentes com log de aviso
- [x] 🔴 **1.2b** `core/dedupe.py` — deduplicação por EAN (`"Código"`) via Polars
- [x] 🔴 **1.3** `core/diff.py` — filtragem de não cadastrados contra união de `"Código"` e `"Código de barras"` do espelho
- [x] 🟡 **1.4** `core/build_import.py` — helper de exportação final para o layout Microvix
- [x] 🔴 **1.5** `core/parser.py` — extração e higienização de modelos (`extrair_modelos_planilha`), EANs de planilhas (`extrair_eans_planilha`) e XMLs de NFe (`extrair_eans_xml`)
- [x] 🟢 **1.6** Testes unitários para os módulos do `core/` (dados simulados com pytest — 100% passando)

---

## Fase 2 — Mirror stub (100% CONCLUÍDA)

- [x] 🔴 **2.1** `core/mirror_sync.py` — carregamento do XLSX da Microvix via `calamine` com `schema_overrides={"Código": pl.String, "Código de barras": pl.String}`
- [x] 🔴 **2.2** `core/mirror_repo.py` — simplificado/descartado em favor do diff vetorial direto em memória no Polars

---

## Fase 3 — Entrypoints e CLI (integração dos fluxos) (100% CONCLUÍDA)

- [x] 🟡 **3.1** `entrypoints/fluxo_colecao.py` — orquestração completa do fluxo de coleção com gravação em `results/` e `results/check/`
- [x] 🟡 **3.1b** `entrypoints/fluxo_divergentes.py` — orquestração da conciliação direta de itens divergentes contra a Microvix
- [x] 🟡 **3.2** `entrypoints/fluxo_nfe.py` — parse do XML (DANFE/NFe) → extração de EANs → `empresa_repo.buscar_por_ean` → `diff` → exportação
- [x] 🟡 **3.3** `main.py` — interface CLI oficial com **Typer**, expondo subcomandos `colecao`, `divergentes` e `nfe`, opções `-n`, `-p`, `-b`, `-x`, help contextual e inicialização de logs
- [x] 🟢 **3.4** Tratamento de erro amigável na CLI (mensagens customizadas para arquivo inexistente, erro de validação e exceptions gerais)

---

## Fase 4 — Validação com dados reais (100% CONCLUÍDA)

- [x] 🟡 **4.1** Validação operacional com planilha de coleção real de grande volume (execução em segundos validada)
- [x] 🟡 **4.2** Validação operacional com planilha de divergentes (`a_verificar.xlsx`) via comando `python main.py divergentes`
- [x] 🟡 **4.3** Validação do fluxo de XML de NFe via comando `python main.py nfe`
- [x] 🟢 **4.4** Validação dos arquivos gerados em `results/` para importação direta no ERP MICROVIX

---

## Fase 5 — Decisão Técnica sobre o `mirror_sync` (100% CONCLUÍDA)

- [x] 🟡 **5.1** Investigação de endpoints de exportação da Microvix (`/api/ExportadorDados/PublicarSolicitacaoNaFila`)
- [x] 🟢 **5.2** Avaliação de automação síncrona: **Descartada**. A fila de exportação da Microvix leva ~20+ minutos para gerar o arquivo de 500k produtos, o que tornaria a execução da CLI bloqueante e inviável.
- [x] 🟢 **5.3** Decisão arquitetural consolidada: **Manutenção do espelho local em memória (`mirror_stub`)**. O usuário atualiza a planilha base periodicamente e o Data Reconcilier executa as validações e anti-joins instantaneamente (em ~1-3s).

---

## Backlog / Futuro (Opcional)

- [ ] 🔵 Automação agendada em segundo plano (cron/worker noturno) para solicitar e baixar o relatório da Microvix de madrugada
- [ ] 🔵 Empacotamento como executável único (PyInstaller) caso necessário para distribuição em máquinas sem Python
