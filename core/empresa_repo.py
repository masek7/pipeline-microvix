import oracledb
import polars as pl
from infra.sql_loader import sql_ean
from itertools import batched



def gerar_placeholders(quantidade: int) -> str:
    """função que gera os string de placeholders"""
    return ", ".join([f":{i+1}" for i in range(quantidade)])

def buscar_por_modelo(modelo: list[str], conn: oracledb.Connection ) -> pl.DataFrame:

    dfs = []
    columns = None
    query = sql_ean

    with conn.cursor() as cursor:

        for chunk in batched(modelo, 900):

            placeholders = gerar_placeholders(len(chunk))
            query_final = query.format(modelo_placeholders=placeholders)

            cursor.execute(query_final, chunk)

            if columns is None:
                columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()

            if rows:
                dfs.append(pl.DataFrame(rows, schema = columns, orient= 'row' ))

    return pl.concat(dfs) if dfs else pl.DataFrame()

