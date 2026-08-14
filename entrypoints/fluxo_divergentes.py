import polars as pl
from datetime import datetime
from core.diff import diff_base
from core.mirror_sync import mirror_stub
from infra.log_config import setup_logging
from pathlib import Path
import logging

data = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
logger = logging.getLogger(__name__)


def executar_fluxo_divergentes( nome_arquivo:str, caminho_planilha_produtos: Path = Path(r'C:\Users\guilherme.morais\PycharmProjects\data_reconcilier\entrypoints\a_verificar.xlsx'), caminho_base_microvix: Path = Path(r'C:\Users\guilherme.morais\Documents\Base_microvix.xlsx')):
    try:

        df_candidatos = pl.read_excel(caminho_planilha_produtos)
        df_microvix = mirror_stub(caminho_base_microvix)

        df_nao_cadastrados = diff_base(df_candidatos, df_microvix)
        logger.info("Produtos não cadastrados: %d", df_nao_cadastrados.height)

        df_nao_cadastrados.write_excel(workbook=f"data_reconcilier/results/{nome_arquivo}_{data}_não_cadastrados.xlsx")

        return df_nao_cadastrados
    except Exception as e:
        logger.error("Erro ao executar fluxo de coleção: %s", e)
        raise


if __name__ == "__main__":
    setup_logging(nome_arquivo="colecao_divergentes")

    logger.info("Iniciando execução do fluxo de coleta.")
    df = executar_fluxo_divergentes('colecao_divergentes')
    logger.info("Execução do fluxo de coleta concluída.")
