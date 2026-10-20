from datetime import datetime, timedelta
from bot_trm_usd.src.config.logger_config import logger
import time

def esperar_hora_proceso(hora_objetivo, minuto_objetivo):
    """Espera hasta la hora objetivo para iniciar el proceso"""
    ahora = datetime.now()
    objetivo = ahora.replace(hour=hora_objetivo, minute=minuto_objetivo, second=0, microsecond=0)
    
    if ahora >= objetivo:
        objetivo += timedelta(days=1)
    
    tiempo_espera = (objetivo - ahora).total_seconds()
    logger.info(f"Esperando hasta las {objetivo.strftime('%H:%M:%S')} para iniciar el proceso...")
    time.sleep(tiempo_espera)
    logger.info("Hora objetivo alcanzada. Iniciando proceso...")
