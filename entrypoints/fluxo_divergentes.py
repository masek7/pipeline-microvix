import polars as pl
import logging
from datetime import datetime
from core.diff import diff_base
from core.mirror_sync import mirror_stub

from pathlib import Path


data = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
logger = logging.getLogger(__name__)


def executar_fluxo_divergentes(nome_arquivo: str, caminho_planilha_produtos: Path, caminho_base_microvix: Path) -> pl.DataFrame:
    try:
        df_candidatos = pl.read_excel(caminho_planilha_produtos)
        df_microvix = mirror_stub(caminho_base_microvix)

        df_nao_cadastrados = diff_base(df_candidatos, df_microvix)
        logger.info("Produtos não cadastrados: %d", df_nao_cadastrados.height)

        Path("results").mkdir(parents=True, exist_ok=True)
        caminho_saida = Path("results") / f"{nome_arquivo}_{data}_não_cadastrados.xlsx"

        df_nao_cadastrados.write_excel(workbook=caminho_saida)

        return df_nao_cadastrados
    except Exception as e:
        logger.error("Erro ao executar fluxo de divergentes: %s", e)
        raise
