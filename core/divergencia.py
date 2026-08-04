import logging
import polars as pl

logger = logging.getLogger(__name__)


def verifica_divergencia(df: pl.DataFrame)-> tuple[pl.DataFrame, pl.DataFrame]:

    condicao_divergencia = pl.any_horizontal(
        pl.all().exclude("Código", "Coleção").n_unique().over("Código") > 1
    )

    df_divergentes = df.filter(condicao_divergencia)
    df_limpo = df.filter(~condicao_divergencia)

    if not df_divergentes.is_empty():
        eans_divergentes = df_divergentes.select("Código").unique().to_series().to_list()
        logger.warning(
            f"Foram identificados {len(eans_divergentes)} EANs com divergências."
            f"Encontradas divergências para os seguintes EANs: {eans_divergentes[:5]}")



    return df_limpo, df_divergentes


