import polars as pl
import pytest
from core.divergencia import verifica_divergencia


def test_divergencia_ignora_variacao_em_colecao():
    # O mesmo EAN001 possui coleções diferentes, mas o resto é idêntico
    df = pl.DataFrame({
        "Código": ["EAN001", "EAN001"],
        "Descrição": ["Camisa", "Camisa"],
        "Preço": [50.0, 50.0],
        "Coleção": ["Verão 2025", "Inverno 2025"]
    })

    df_limpo, df_divergentes = verifica_divergencia(df)

    assert df_limpo.height == 2
    assert df_divergentes.is_empty()


def test_divergencia_identifica_variacao_em_outras_colunas():
    # EAN001 tem preços diferentes -> deve ir para df_divergentes
    # EAN002 é consistente -> deve ficar no df_limpo
    df = pl.DataFrame({
        "Código": ["EAN001", "EAN001", "EAN002", "EAN002"],
        "Descrição": ["Camisa", "Camisa", "Calça", "Calça"],
        "Preço": [50.0, 80.0, 100.0, 100.0],
        "Coleção": ["Verão 2025", "Verão 2025", "Inverno 2025", "Inverno 2025"]
    })

    df_limpo, df_divergentes = verifica_divergencia(df)

    assert df_limpo.height == 2
    assert df_limpo["Código"].unique().to_list() == ["EAN002"]

    assert df_divergentes.height == 2
    assert df_divergentes["Código"].unique().to_list() == ["EAN001"]


def test_divergencia_dataframe_vazio():
    df = pl.DataFrame({
        "Código": [],
        "Descrição": [],
        "Coleção": []
    }, schema={"Código": pl.String, "Descrição": pl.String, "Coleção": pl.String})

    df_limpo, df_divergentes = verifica_divergencia(df)

    assert df_limpo.is_empty()
    assert df_divergentes.is_empty()
