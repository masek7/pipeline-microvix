import polars as pl
def dedupe(df: pl.DataFrame)-> pl.DataFrame:
    return df.unique(subset=["Código"])
