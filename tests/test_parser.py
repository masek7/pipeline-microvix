import polars as pl
import pytest
from core.parser import extrair_modelos_planilha, extrair_eans_planilha


def test_extrair_modelos_planilha_sucesso(tmp_path):
    arquivo_excel = tmp_path / "modelos.xlsx"
    df = pl.DataFrame({
        "Modelo": ["MOD001", "MOD002 ", None, "MOD001", "  MOD003  "],
        "Descricao": ["A", "B", "C", "D", "E"]
    })
    df.write_excel(arquivo_excel)

    resultado = extrair_modelos_planilha(str(arquivo_excel), coluna_modelo="Modelo")

    # Deve remover nulos, duplicados e espaços
    assert sorted(resultado) == ["MOD001", "MOD002", "MOD003"]


def test_extrair_modelos_planilha_coluna_ausente(tmp_path):
    arquivo_excel = tmp_path / "modelos_sem_coluna.xlsx"
    df = pl.DataFrame({
        "OutraColuna": ["MOD001", "MOD002"]
    })
    df.write_excel(arquivo_excel)

    with pytest.raises(ValueError, match="A planilha não contém a coluna obrigatória 'Modelo'"):
        extrair_modelos_planilha(str(arquivo_excel), coluna_modelo="Modelo")


def test_extrair_eans_planilha_sucesso(tmp_path):
    arquivo_excel = tmp_path / "eans.xlsx"
    df = pl.DataFrame({
        "Código": ["7890001", " 7890002 ", None, "7890001"],
        "Tamanho": [34, 35, 36, 37]
    })
    df.write_excel(arquivo_excel)

    resultado = extrair_eans_planilha(str(arquivo_excel), coluna_ean="Código")

    assert sorted(resultado) == ["7890001", "7890002"]


def test_extrair_eans_planilha_coluna_ausente(tmp_path):
    arquivo_excel = tmp_path / "eans_sem_coluna.xlsx"
    df = pl.DataFrame({
        "EAN_Invalido": ["7890001"]
    })
    df.write_excel(arquivo_excel)

    with pytest.raises(ValueError, match="A planilha não contém a coluna obrigatória 'Código'"):
        extrair_eans_planilha(str(arquivo_excel), coluna_ean="Código")
