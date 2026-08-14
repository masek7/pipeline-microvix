import oracledb
import polars as pl
import logging
from infra.sql_loader import sql_modelo, sql_ean
from itertools import batched

logger = logging.getLogger(__name__)

def gerar_placeholders(quantidade: int) -> str:
    """função que gera os string de placeholders"""
    return ", ".join([f":{i+1}" for i in range(quantidade)])

def buscar_por_modelo(modelo: list[str], conn: oracledb.Connection ) -> pl.DataFrame:

    dfs = []
    columns = None
    query = sql_modelo

    with conn.cursor() as cursor:
        logger.info("Buscando produtos por modelo.")
        total_linhas = 0
        for chunk in batched(modelo, 900):

            placeholders = gerar_placeholders(len(chunk))
            query_final = query.format(modelo_placeholders=placeholders)

            cursor.execute(query_final, chunk)

            if columns is None:
                columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()

            if rows:
                dfs.append(pl.DataFrame(rows, schema = columns, orient= 'row' ))
                total_linhas += len(rows)

        logger.info("Processados %d produtos.", total_linhas)

    return pl.concat(dfs) if dfs else pl.DataFrame()

def buscar_por_ean(ean: list[str], conn: oracledb.Connection ) -> pl.DataFrame:

    dfs = []
    columns = None
    query = sql_ean

    with conn.cursor() as cursor:
        logger.info("Buscando produtos por ean.")
        total_linhas = 0
        for chunk in batched(ean, 900):

            placeholders = gerar_placeholders(len(chunk))
            query_final = query.format(ean_placeholders=placeholders)

            cursor.execute(query_final, chunk)

            if columns is None:
                columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()

            if rows:
                dfs.append(pl.DataFrame(rows, schema = columns, orient= 'row' ))
                total_linhas += len(rows)

        logger.info("Processados %d produtos.", total_linhas)

    return pl.concat(dfs) if dfs else pl.DataFrame()

