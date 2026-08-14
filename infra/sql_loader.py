from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"

sql_modelo = (SQL_DIR / "busca_por_modelo.sql").read_text(encoding="utf-8")
sql_ean = (SQL_DIR / "busca_por_ean.sql").read_text(encoding="utf-8")