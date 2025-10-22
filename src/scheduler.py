# src/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from logger import get_logger
from config import Config
import time

logger = get_logger()

def tarea_prueba():
    """Ejemplo de tarea automática programada."""
    logger.info(f"Tarea ejecutada automáticamente a las {datetime.now()}")

def iniciar_scheduler():
    """Inicia el planificador en segundo plano."""
    logger.info("Iniciando scheduler de tareas...")

    scheduler = BackgroundScheduler(timezone="America/Bogota")

    # Ejemplo: ejecuta tarea cada 30 segundos
    scheduler.add_job(tarea_prueba, "interval", seconds=30, id="tarea_prueba")

    scheduler.start()
    logger.info("Scheduler iniciado correctamente.")

    try:
        # Mantener el scheduler corriendo
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Deteniendo scheduler...")
        scheduler.shutdown()

if __name__ == "__main__":
    iniciar_scheduler()