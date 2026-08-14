from core.parser import extrair_modelos_planilha
from core.empresa_repo import buscar_por_modelo
from core.divergencia import verifica_divergencia
from core.dedupe import dedupe
from core.diff import diff_base
from core.mirror_sync import mirror_stub
from infra.oracle import get_connection
from infra.log_config import setup_logging
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def executar_fluxo_colecao(nome_arquivo: str, caminho_planilha_modelos: Path = Path(r'C:\Users\guilherme.morais\Downloads\Microvix.xlsx'), caminho_base_microvix: Path = Path(r'C:\Users\guilherme.morais\Documents\Base_microvix.xlsx')):

    try:
        modelos = extrair_modelos_planilha(caminho_planilha_modelos)

        df_microvix = mirror_stub(caminho_base_microvix)

        with get_connection() as conn:
            df_oracle = buscar_por_modelo(modelos, conn)

        df_limpo, df_divergentes = verifica_divergencia(df_oracle)
        df_candidatos = dedupe(df_limpo)
        df_a_verificar = df_divergentes
        
        logger.info("Produtos não cadastrados: %d, Produtos a verificar: %d", df_candidatos.height, df_a_verificar.height)

        df_nao_cadastrados = diff_base(df_candidatos, df_microvix)

        df_nao_cadastrados.write_excel(workbook=f"data_reconcilier/results/{nome_arquivo}_não_cadastrados.xlsx")
        df_a_verificar.write_excel(workbook=f"data_reconcilier/results/check/{nome_arquivo}_a_verificar.xlsx")

        return df_nao_cadastrados, df_a_verificar
    except Exception as e:
        logger.error("Erro ao executar fluxo de coleção: %s", e)
        raise

if __name__ == "__main__":
    setup_logging(nome_arquivo="colecao_2627")
    logger.info("Iniciando execução do fluxo de coleta.")
    df = executar_fluxo_colecao(nome_arquivo="colecao")
    logger.info("Execução do fluxo de coleta concluída.")
