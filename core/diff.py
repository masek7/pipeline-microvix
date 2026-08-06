import polars as pl

def diff_base(candidatos: pl.DataFrame, base_microvix: pl.DataFrame) -> pl.DataFrame:

    df_final = candidatos.join(base_microvix, on="Código", how="anti")

    return df_final


