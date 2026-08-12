import polars as pl

def extrair_modelos_planilha(caminho_planilha: str, coluna_modelo: str = "Modelo") -> list[str]:

    df = pl.read_excel(caminho_planilha, engine="calamine")

    if coluna_modelo not in df.columns:
        raise ValueError(f"A planilha não contém a coluna '{coluna_modelo}'.")

    return (
        df.select(coluna_modelo)
        .drop_nulls()
        .to_series()
        .cast(pl.String)
        .str.strip_chars()
        .unique()
        .to_list()
    )