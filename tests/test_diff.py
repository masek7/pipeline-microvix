import polars as pl
import pytest
from core.diff import diff_base


def test_diff_base_identifica_produtos_nao_cadastrados():
    candidatos = pl.DataFrame({
        "Código": ["EAN001", "EAN002", "EAN003"],
        "Descrição": ["Produto 1", "Produto 2", "Produto 3"]
    })

    # Mirror contendo EAN001 em "Código" e EAN002 em "Código de barras"
    mirror = pl.DataFrame({
        "Código": ["EAN001", "EAN999"],
        "Código de barras": ["EAN888", "EAN002"]
    })

    resultado = diff_base(candidatos, mirror)

    # Apenas EAN003 deve sobrar
    assert resultado.height == 1
    assert resultado["Código"].to_list() == ["EAN003"]


def test_diff_base_candidatos_vazio():
    candidatos = pl.DataFrame({"Código": []}, schema={"Código": pl.String})
    mirror = pl.DataFrame({
        "Código": ["EAN001"],
        "Código de barras": ["EAN002"]
    })

    resultado = diff_base(candidatos, mirror)
    assert resultado.is_empty()


def test_diff_base_mirror_vazio():
    candidatos = pl.DataFrame({
        "Código": ["EAN001", "EAN002"]
    })
    mirror = pl.DataFrame({
        "Código": [],
        "Código de barras": []
    }, schema={"Código": pl.String, "Código de barras": pl.String})

    resultado = diff_base(candidatos, mirror)
    assert resultado.height == 2
    assert resultado["Código"].to_list() == ["EAN001", "EAN002"]


def test_diff_base_todos_produtos_ja_existem():
    candidatos = pl.DataFrame({
        "Código": ["EAN001", "EAN002"]
    })
    mirror = pl.DataFrame({
        "Código": ["EAN001", "EAN002"],
        "Código de barras": [None, None]
    })

    resultado = diff_base(candidatos, mirror)
    assert resultado.is_empty()
