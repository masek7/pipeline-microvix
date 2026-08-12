import polars as pl
import logging

logger = logging.getLogger(__name__)

def dedupe(df: pl.DataFrame)-> pl.DataFrame:

    try:
        if df.is_empty():
            logger.info("O DataFrame está vazio. Nenhuma deduplicação necessária.")
            return pl.DataFrame()

        elif "Código" not in df.columns:
            logger.error("A coluna 'Código' não está presente no DataFrame. Não é possível realizar a deduplicação.")
            raise ValueError("A coluna 'Código' não está presente no DataFrame para deduplicação.")

    except Exception as e:
        logger.error("Erro ao realizar deduplicação: %s", e)
        raise

    logger.info("Deduplicação realizada com sucesso.")
    return df.unique(subset=["Código"])
