import polars as pl
import logging

logger = logging.getLogger(__name__)

def extrair_modelos_planilha(caminho_planilha: str, coluna_modelo: str = "Modelo") -> list[str]:

    try:
        df = pl.read_excel(caminho_planilha, engine="calamine")
        logger.info("Planilha lida com sucesso.")
        if coluna_modelo not in df.columns:
            logger.warning("A planilha não contém a coluna '%s'.", coluna_modelo)
            raise ValueError(f"A planilha não contém a coluna obrigatória '{coluna_modelo}'.")
    except Exception as e:
        logger.error("Erro ao ler a planilha: %s", e)
        raise


    return (
        df.select(coluna_modelo)
        .drop_nulls()
        .to_series()
        .cast(pl.String)
        .str.strip_chars()
        .unique()
        .to_list()
    )