# Data Reconcilier

Pipeline em Python para conciliar e validar produtos entre o banco de dados interno
(**EMPRESA / Oracle**) e o catálogo do ERP **MICROVIX** (~500 mil produtos).

O objetivo é identificar quais produtos — vindos de planilhas de coleção de modelos,
planilhas de divergências (EANs) ou, futuramente, notas fiscais XML — ainda **não existem**
na base da Microvix, e gerar um Excel (`.xlsx`) no layout aceito pela importação nativa do ERP.

> Para o racional completo de arquitetura e decisões de design, veja [`docs/context.md`](docs/context.md).
> Para o status detalhado por fase, veja [`docs/roadmap_pipeline_microvix.md`](docs/roadmap_pipeline_microvix.md).

---

## Arquitetura em uma frase

`entrypoints` orquestra, `core` decide (funções puras, sem I/O), `infra` conversa com o
mundo externo (Oracle, arquivos de log, variáveis de ambiente). Nenhum módulo de `core`
depende de Typer, Oracle ou sistema de arquivos diretamente.

```
Planilha / EAN ──▶ core/parser.py ──▶ core/empresa_repo.py (Oracle)
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
- Um export `.xlsx` atualizado do catálogo Microvix (usado como espelho local)

---

## Instalação

```bash
git clone <repo>
cd data-reconcilier
uv sync
```

## Configuração

Copie `.env.example` para `.env` e preencha:

```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_SERVICE=nome_do_servico
ORACLE_CLIENT_LIB_DIR=/caminho/para/instantclient
```

---

## Uso

O ponto de entrada oficial é `main.py`, via [Typer](https://typer.tiangolo.com/).

### Fluxo de coleção (busca no Oracle por modelo)

```bash
python main.py colecao \
  --nome-arquivo minha_colecao \
  --caminho-planilha-modelos data/modelos.xlsx \
  --caminho-base-microvix data/microvix_espelho.xlsx
```

Gera:
- `results/<nome>_<timestamp>_não_cadastrados.xlsx` — candidatos prontos para importação
- `results/check/<nome>_<timestamp>_a_verificar.xlsx` — divergências que precisam de revisão manual

### Fluxo de divergentes (conciliação direta por EAN)

```bash
python main.py divergentes \
  --nome-arquivo minha_verificacao \
  --caminho-planilha-produtos a_verificar.xlsx \
  --caminho-base-microvix data/microvix_espelho.xlsx
```

Gera `results/<nome>_<timestamp>_não_cadastrados.xlsx`.

Cada execução também grava um log com timestamp em `logs`.

---

## Estrutura de pastas

```
core/           # regras de negócio puras (parser, diff, dedupe, divergência, repo Oracle)
entrypoints/    # orquestração dos fluxos (colecao, divergentes)
infra/          # config (.env), conexão Oracle, logging, carregamento de SQL
sql/            # queries Oracle usadas por core/empresa_repo.py
results/        # saídas geradas (não versionado)
  └── check/    # itens retidos para revisão manual
logs/           # logs de execução (não versionado)
```

---

## Status do projeto

| Fase | Descrição | Status |
|---|---|---|
| 0 | Setup do projeto | ✅ quase completo (falta smoke test) |
| 1 | Núcleo independente do mirror | ✅ completo (falta cobertura de testes) |
| 2 | Mirror stub (Excel local) | ✅ completo — sync **manual** |
| 3 | Entrypoints e CLI | 🟡 em andamento (falta `fluxo_nfe.py` e tratamento de erro amigável) |
| 4 | Validação com dados reais | ⏳ não iniciado |
| 5 | Automação real do `mirror_sync` | ⏳ não iniciado |

Detalhes item a item em [`docs/roadmap_pipeline_microvix.md`](docs/roadmap_pipeline_microvix.md).

---

## Diretrizes para contribuição

- Manter funções em `core` puras (sem I/O direto), com tipagem explícita.
- Novas queries Oracle vão em `sql` e são carregadas via `infra/sql_loader.py`.
- Toda mudança de fluxo de negócio deve ser refletida em `docs/context.md` e no roadmap.
- Preferir extensão de `entrypoints` a lógica nova dentro de `main.py`.