import logging
import sys
import time
from pathlib import Path

def setup_logging(nome_arquivo: str | None = None, diretorio_logs: str | Path = "data_reconcilier/logs", nivel: int = logging.INFO) -> None:

    logging.getLogger().handlers.clear()  # Limpa os handlers existentes

    Path(diretorio_logs).mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    if nome_arquivo:
        log_file = Path(diretorio_logs) / f"{nome_arquivo}_{timestamp}.log"
    else:
        log_file = Path(diretorio_logs) / f"app_{timestamp}.log"

    logging.basicConfig(
        level=nivel,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )