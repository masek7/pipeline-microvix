import logging
import polars as pl

logger = logging.getLogger(__name__)


def verifica_divergencia(df: pl.DataFrame)-> tuple[pl.DataFrame, pl.DataFrame]:

    try:
        condicao_divergencia = pl.any_horizontal(
            pl.all().exclude("Código", "Coleção").n_unique().over("Código") > 1
        )

        df_divergentes = df.filter(condicao_divergencia)
        df_limpo = df.filter(~condicao_divergencia)

        if not df_divergentes.is_empty():
            eans_divergentes = df_divergentes.select("Código").unique().to_series().to_list()
            logger.warning("Identificados %d produtos divergentes no catálogo local: %s", len(eans_divergentes), eans_divergentes[:10])

    except Exception as e:
        logger.error("Erro ao verificar divergências: %s", e)
        raise

    logger.info("Verificação de divergências concluída. Produtos divergentes: %d, Produtos limpos: %d", df_divergentes.height, df_limpo.height)

    return df_limpo, df_divergentes


