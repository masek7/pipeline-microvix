import polars as pl
def dedupe(df: pl.DataFrame)-> pl.DataFrame:

    if df.is_empty():
        return pl.DataFrame()
    elif "Código" not in df.columns:
        raise ValueError("A coluna 'Código' é necessária para a deduplicação.")

    return df.unique(subset=["Código"])
