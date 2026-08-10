import polars as pl


def mirror_stub(caminho_base: str) -> pl.DataFrame:


    df_base = pl.read_excel(
        caminho_base,
        engine="calamine",
        columns= ["Código"],
        schema_overrides={"Código": pl.String}
    )
    return df_base
