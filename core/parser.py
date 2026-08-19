import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import polars as pl

logger = logging.getLogger(__name__)

def extrair_modelos_planilha(caminho_planilha: Path, coluna_modelo: str = "Modelo") -> list[str]:

    try:
        df = pl.read_excel(caminho_planilha, engine="calamine")
        logger.info("Planilha lida com sucesso.")
        if coluna_modelo not in df.columns:
            logger.warning("A planilha não contém a coluna '%s'.", coluna_modelo)
            raise ValueError(f"A planilha não contém a coluna obrigatória '{coluna_modelo}'.")
    except Exception as e:
        logger.error("Erro ao ler a planilha: %s", e)
        raise

    return (
        df.select(coluna_modelo)
        .drop_nulls()
        .to_series()
        .cast(pl.String)
        .str.strip_chars()
        .unique()
        .to_list()
    )

def extrair_eans_planilha(caminho_planilha: Path, coluna_ean: str = "Código") -> list[str]:

    try:
        df = pl.read_excel(caminho_planilha, engine="calamine")
        logger.info("Planilha lida com sucesso.")
        if coluna_ean not in df.columns:
            logger.warning("A planilha não contém a coluna '%s'.", coluna_ean)
            raise ValueError(f"A planilha não contém a coluna obrigatória '{coluna_ean}'.")
    except Exception as e:
        logger.error("Erro ao ler a planilha: %s", e)
        raise

    return (
        df.select(coluna_ean)
        .drop_nulls()
        .to_series()
        .cast(pl.String)
        .str.strip_chars()
        .unique()
        .to_list()
    )

def extrair_eans_xml(caminho_xml: Path | str) -> list[str]:
    caminho = Path(caminho_xml)
    try:
        xml_content = caminho.read_text(encoding="utf-8")
        # Remove namespace padrão para simplificar a busca de tags
        xml_content = re.sub(r'xmlns="[^"]+"', '', xml_content, count=1)
        root = ET.fromstring(xml_content)

        dets = root.findall('.//det')
        if not dets:
            logger.warning("Nenhum item de produto (<det>) encontrado no XML: %s", caminho)
            raise ValueError(f"Nenhum item de produto (<det>) foi encontrado no arquivo XML '{caminho.name}'.")

        eans = []
        for det in dets:
            prod = det.find('prod')
            if prod is None:
                continue

            cean_elem = prod.find('cEAN')
            if cean_elem is not None and cean_elem.text:
                cean = cean_elem.text.strip()
                if cean and cean.upper() != "SEM GTIN":
                    eans.append(cean)

        # Remove duplicados preservando a ordem
        eans_unicos = list(dict.fromkeys(eans))
        logger.info("XML de NFe lido com sucesso. Total de %d EANs únicos extraídos.", len(eans_unicos))
        return eans_unicos

    except ET.ParseError as e:
        logger.error("Erro de parsing no arquivo XML %s: %s", caminho, e)
        raise ValueError(f"O arquivo XML '{caminho.name}' possui estrutura inválida ou corrompida: {e}")
    except Exception as e:
        logger.error("Erro ao extrair EANs do XML %s: %s", caminho, e)
        raise