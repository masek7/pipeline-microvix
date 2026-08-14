import polars as pl
import pytest
from core.dedupe import dedupe


def test_dedupe_remove_duplicidades_por_codigo():
    df = pl.DataFrame({
        "Código": ["EAN001", "EAN001", "EAN002"],
        "Descrição": ["Produto A", "Produto A", "Produto B"]
    })

    resultado = dedupe(df)

    assert resultado.height == 2
    assert sorted(resultado["Código"].to_list()) == ["EAN001", "EAN002"]


def test_dedupe_dataframe_vazio():
    df = pl.DataFrame()
    resultado = dedupe(df)
    assert resultado.is_empty()


def test_dedupe_dataframe_vazio_com_schema():
    df = pl.DataFrame({"Código": []}, schema={"Código": pl.String})
    resultado = dedupe(df)
    assert resultado.is_empty()


def test_dedupe_lanca_value_error_quando_sem_coluna_codigo():
    df = pl.DataFrame({
        "Nome": ["Item 1", "Item 2"],
        "Preco": [10.0, 20.0]
    })

    with pytest.raises(ValueError, match="A coluna 'Código' não está presente"):
        dedupe(df)
