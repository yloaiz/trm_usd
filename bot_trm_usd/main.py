import argparse
import time

import bot_trm_usd.src.correo.config_correo as datos_correo
from bot_trm_usd.src.config.logger_config import logger
from bot_trm_usd.src.correo.enviar_correo import (
    enviar_correo_notificacion_exitosa,
    enviar_correo_notificacion_fallido,
)
from bot_trm_usd.src.procesos.lectura_json import lecturas_y_envio_datos_json
from bot_trm_usd.src.servicio_banrep.servicio_banrep import servicio_datos_banrep
from bot_trm_usd.src.utils.crear_json import crear_json
from bot_trm_usd.src.utils.esperar_hora_proceso import esperar_hora_proceso
from bot_trm_usd.src.utils.limpiar_json import limpiar_archivos_json

# Configuración de reintentos
MAX_INTENTOS = 2
TIEMPO_ESPERA_REINTENTO = 300  # 5 minutos en segundos


def ejecutar_proceso() -> None:
    """Ejecuta el flujo principal de extracción, generación de JSON y envío."""
    try:
        # 1. Limpieza de archivos temporales
        limpiar_archivos_json()
        time.sleep(2)

        # 2. Extracción de datos del Banco de la República
        tasa = servicio_datos_banrep()
        logger.info("Tasa obtenida: %s", tasa)
        crear_json(tasa)

        # 3. Envío de información al ESB
        # lecturas_y_envio_datos_json()

        # 4. Notificación exitosa
        try:
            destinatario = datos_correo.destinatario_correo
            asunto = datos_correo.asunto_correo
            enviar_correo_notificacion_exitosa(destinatario, asunto)
        except Exception:
            logger.exception(
                "Los datos fueron procesados, pero falló la notificación por correo de éxito. "
                "No se repetirá el proceso por este motivo."
            )

    except Exception as e:
        logger.error("Error durante la ejecución del proceso: %s", e)

        # Intentar enviar notificación de fallo
        try:
            destinatario = datos_correo.destinatario_correo
            asunto = datos_correo.asunto_correo
            cuerpo = datos_correo.cuerpo_proceso_fallido
            enviar_correo_notificacion_fallido(destinatario, asunto, cuerpo)
        except Exception:
            logger.exception("Falló también el correo de notificación de error.")

        # Re-lanzar para que el manejador de reintentos capture la excepción
        raise


def ejecutar_con_reintentos() -> bool:
    """Maneja el bucle de reintentos para una ejecución diaria."""
    for intento in range(1, MAX_INTENTOS + 1):
        try:
            logger.info(f"Iniciando ejecución del proceso (intento {intento}/{MAX_INTENTOS})")
            ejecutar_proceso()
            logger.info("Proceso finalizado correctamente.")
            return True

        except Exception as e:
            logger.error(f"Error en el intento {intento}/{MAX_INTENTOS}: {e}")

            if intento < MAX_INTENTOS:
                logger.info(f"Esperando {TIEMPO_ESPERA_REINTENTO // 60} minutos antes de reintentar...")
                time.sleep(TIEMPO_ESPERA_REINTENTO)
            else:
                logger.error("Se agotaron los intentos permitidos para la ejecución actual.")
    
    return False


def flujo_bucle_diario():
    """Bucle infinito para ejecución programada en servicio continuo."""
    while True:
        try:
            # Espera la hora programada (ej. 5:15 AM)
            esperar_hora_proceso(12, 37)
            
            ejecutar_con_reintentos()
            
            logger.info("Ciclo diario completado. Esperando la siguiente ventana de ejecución...")

        except Exception as e:
            logger.error(f"Error general en el ciclo diario: {e}", exc_info=True)

        time.sleep(60)


def main():
    """Punto de entrada principal que invoca el comando trm_usd."""
    parser = argparse.ArgumentParser(description="Proceso de extracción y notificación Banrep")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ejecuta el proceso una sola vez inmediatamente y finaliza (útil para Cron/Tareas programadas)."
    )
    args = parser.parse_args()

    if args.once:
        logger.info("Modo de ejecución única activado (--once).")
        exito = ejecutar_con_reintentos()
        if not exito:
            exit(1)
    else:
        logger.info("Iniciando servicio en modo bucle diario...")
        flujo_bucle_diario()


if __name__ == "__main__":
    main()