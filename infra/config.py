from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    oracle_host: str
    oracle_port: int
    oracle_user: str
    oracle_password: str
    oracle_service: str
    oracle_client_lib_dir: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )

settings = Settings()