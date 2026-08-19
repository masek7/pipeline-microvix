import polars as pl
import pytest
from core.parser import extrair_modelos_planilha, extrair_eans_planilha, extrair_eans_xml


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


def test_extrair_eans_xml_sucesso(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
        <NFe>
            <infNFe Id="NFe123">
                <det nItem="1">
                    <prod>
                        <cEAN>7891111111111</cEAN>
                        <xProd>PRODUTO 1</xProd>
                    </prod>
                </det>
                <det nItem="2">
                    <prod>
                        <cEAN> 7892222222222 </cEAN>
                        <xProd>PRODUTO 2</xProd>
                    </prod>
                </det>
                <det nItem="3">
                    <prod>
                        <cEAN>7891111111111</cEAN>
                        <xProd>PRODUTO 1 REPETIDO</xProd>
                    </prod>
                </det>
                <det nItem="4">
                    <prod>
                        <cEAN>SEM GTIN</cEAN>
                        <xProd>SERVIÇO SEM EAN</xProd>
                    </prod>
                </det>
            </infNFe>
        </NFe>
    </nfeProc>"""
    arquivo_xml = tmp_path / "nfe_teste.xml"
    arquivo_xml.write_text(xml_content, encoding="utf-8")

    resultado = extrair_eans_xml(arquivo_xml)

    assert resultado == ["7891111111111", "7892222222222"]


def test_extrair_eans_xml_sem_itens(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
        <NFe>
            <infNFe Id="NFe123">
            </infNFe>
        </NFe>
    </nfeProc>"""
    arquivo_xml = tmp_path / "nfe_vazia.xml"
    arquivo_xml.write_text(xml_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Nenhum item de produto"):
        extrair_eans_xml(arquivo_xml)


def test_extrair_eans_xml_invalido(tmp_path):
    arquivo_xml = tmp_path / "nfe_corrompida.xml"
    arquivo_xml.write_text("<xml>invalido", encoding="utf-8")

    with pytest.raises(ValueError, match="possui estrutura inválida ou corrompida"):
        extrair_eans_xml(arquivo_xml)

