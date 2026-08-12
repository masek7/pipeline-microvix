import polars as pl

def diff_base(candidatos: pl.DataFrame, base_microvix: pl.DataFrame) -> pl.DataFrame:

    codigos_existentes = pl.concat([base_microvix["Código"], base_microvix["Código de barras"]]).drop_nulls().unique()

    resultado = candidatos.filter(~pl.col("Código").is_in(codigos_existentes))

    return resultado


