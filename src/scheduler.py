from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from logger import get_logger
from main import main as ejecutar_sistema
import time

logger = get_logger()

def tarea_automatizada():
    """Tarea programada que ejecuta el sistema completo"""
    logger.info("Ejecutando tarea automatizada programada")
    try:
        ejecutar_sistema()
        logger.info("Tarea automatizada completada exitosamente")
    except Exception as e:
        logger.error(f"Error en tarea automatizada: {e}")

def iniciar_scheduler():
    """Inicia el planificador para ejecutar cada 30 minutos"""
    logger.info("Iniciando scheduler de tareas automaticas")
    
    scheduler = BackgroundScheduler(timezone="America/Bogota")
    
    # Ejecutar cada 30 minutos como requiere la prueba
    scheduler.add_job(
        tarea_automatizada, 
        "interval", 
        minutes=30, 
        id="tarea_principal",
        next_run_time=datetime.now()  # Ejecutar inmediatamente la primera vez
    )
    
    scheduler.start()
    logger.info("Scheduler iniciado correctamente - Ejecutando cada 30 minutos")
    
    try:
        # Mantener el scheduler corriendo
        while True:
            time.sleep(60)  # Revisar cada minuto
            # Opcional: Log cada hora para ver que sigue vivo
            if datetime.now().minute == 0:
                logger.info("Scheduler activo - proxima ejecucion en 30 min")
                
    except (KeyboardInterrupt, SystemExit):
        logger.info("Deteniendo scheduler...")
        scheduler.shutdown()

if __name__ == "__main__":
    iniciar_scheduler()