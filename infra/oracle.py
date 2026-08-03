import oracledb
from contextlib import contextmanager
from infra.config import settings

oracledb.init_oracle_client(
    lib_dir=settings.oracle_client_lib_dir,
)

def build_dsn() -> str:
    return (
        f"{settings.oracle_host}:{settings.oracle_port}/{settings.oracle_service}"
    )

@contextmanager
def get_connection():
    conn = oracledb.connect(
        user=settings.oracle_user,
        password=settings.oracle_password,
        dsn=build_dsn(),
    )
    try:
        yield conn
    finally:
        conn.close()
