# src/logger.py
from loguru import logger
import os
from datetime import datetime

# Crear carpeta de logs si no existe
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Archivo de log rotativo por día
log_filename = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

logger.add(
    log_filename,
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

def get_logger():
    """Devuelve el logger configurado para todo el proyecto."""
    return logger
