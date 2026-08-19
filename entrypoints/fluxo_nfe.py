import logging
from datetime import datetime
from pathlib import Path
import polars as pl

from core.parser import extrair_eans_xml
from core.empresa_repo import buscar_por_ean
from core.divergencia import verifica_divergencia
from core.dedupe import dedupe
from core.diff import diff_base
from core.mirror_sync import mirror_stub
from infra.oracle import get_connection

data = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
logger = logging.getLogger(__name__)


def executar_fluxo_nfe(nome_arquivo: str, caminho_xml: Path, caminho_base_microvix: Path) -> tuple[pl.DataFrame, pl.DataFrame]:
    try:
        eans = extrair_eans_xml(caminho_xml)

        df_microvix = mirror_stub(caminho_base_microvix)

        with get_connection() as conn:
            df_oracle = buscar_por_ean(eans, conn)

        df_limpo, df_divergentes = verifica_divergencia(df_oracle)
        df_candidatos = dedupe(df_limpo)
        df_a_verificar = df_divergentes

        logger.info("Produtos candidatos: %d, Produtos a verificar: %d", df_candidatos.height, df_a_verificar.height)

        df_nao_cadastrados = diff_base(df_candidatos, df_microvix)

        Path("results/check").mkdir(parents=True, exist_ok=True)

        caminho_nao_cadastrados = Path("results") / f"{nome_arquivo}_{data}_não_cadastrados.xlsx"
        caminho_a_verificar = Path("results/check") / f"{nome_arquivo}_{data}_a_verificar.xlsx"

        df_nao_cadastrados.write_excel(workbook=caminho_nao_cadastrados)
        df_a_verificar.write_excel(workbook=caminho_a_verificar)

        return df_nao_cadastrados, df_a_verificar
    except Exception as e:
        logger.error("Erro ao executar fluxo de NFe: %s", e)
        raise
