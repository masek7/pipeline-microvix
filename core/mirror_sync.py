import polars as pl
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def mirror_stub(caminho_base: Path) -> pl.DataFrame:

    try:
        df_base = pl.read_excel(
            caminho_base,
            engine="calamine",
            columns= ["Código", "Código de barras"],
            schema_overrides={"Código": pl.String, "Código de barras": pl.String}
        )
        logger.info("Base espelho Microvix carregada em memória (%d produtos no cátalogo local).", df_base.height)
    except Exception as e:
        logger.error("Erro ao ler a base espelho Microvix: %s", e)
        raise

    return df_base
