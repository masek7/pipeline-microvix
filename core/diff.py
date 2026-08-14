import polars as pl
import logging

logger = logging.getLogger(__name__)

def diff_base(candidatos: pl.DataFrame, base_microvix: pl.DataFrame) -> pl.DataFrame:

    try:
        codigos_existentes = pl.concat([base_microvix["Código"], base_microvix["Código de barras"]]).drop_nulls().unique().to_list()

        resultado = candidatos.filter(~pl.col("Código").is_in(codigos_existentes))

        logger.info("Diferença entre candidatos e base Microvix calculada com sucesso. Produtos não encontrados na base: %d", resultado.height)

    except Exception as e:
        logger.error("Erro ao calcular diferença: %s", e)
        raise

    return resultado


