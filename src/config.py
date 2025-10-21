# src/config.py
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class Config:
    """Clase central de configuración del proyecto."""

    APP_NAME = os.getenv("APP_NAME", "PRUEBA_MISSION")
    ENV = os.getenv("ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.missionsas.com")
    DB_PATH = os.getenv("DB_PATH", "data/database.db")

    @staticmethod
    def summary():
        """Devuelve un resumen legible de la configuración actual."""
        return {
            "APP_NAME": Config.APP_NAME,
            "ENV": Config.ENV,
            "LOG_LEVEL": Config.LOG_LEVEL,
            "API_BASE_URL": Config.API_BASE_URL,
            "DB_PATH": Config.DB_PATH,
        }