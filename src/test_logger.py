# src/test_logger.py

from logger import get_logger

# Inicializa el logger configurado en logger.py
logger = get_logger()

# Mensajes de prueba para verificar que el sistema de logs funciona
logger.info("Prueba de logging inicial")
logger.warning("Esto es una advertencia")
logger.error("Esto es un error de prueba")
