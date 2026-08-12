from core.colecao_parser import extrair_modelos_planilha
from core.empresa_repo import buscar_por_modelo
from core.divergencia import verifica_divergencia
from core.dedupe import dedupe
from core.diff import diff_base
from core.mirror_sync import mirror_stub
from infra.oracle import get_connection


def executar_fluxo_colecao(caminho_planilha_modelos: str, caminho_base_microvix: str):

    modelos = extrair_modelos_planilha(caminho_planilha_modelos)

    df_microvix = mirror_stub(caminho_base_microvix)

    with get_connection() as conn:
        df_oracle = buscar_por_modelo(modelos, conn)

    df_limpo, df_divergentes = verifica_divergencia(df_oracle)
    df_candidatos = dedupe(df_limpo)
    df_a_verificar = df_divergentes

    df_nao_cadastrados = diff_base(df_candidatos, df_microvix)

    return df_nao_cadastrados.write_excel(workbook="não_cadastrados.xlsx"), df_a_verificar.write_excel(workbook="a_verificar.xlsx")


modelo = r'C:\Users\guilherme.morais\Downloads\Microvix.xlsx'
base = r'C:\Users\guilherme.morais\Documents\Base_microvix.xlsx'
if __name__ == "__main__":
    df = executar_fluxo_colecao(modelo, base)

