import os
from bot_trm_usd.src.config.logger_config import logger

def limpiar_archivos_json():
    """
    Elimina los archivos JSON de la carpeta 'descargas' si existen.
    """
    carpeta_descargas = os.path.join(os.getcwd(), "descargas")

    archivos_json = {
        "USD": os.path.join(carpeta_descargas, "moneda_cambio_usd.json"),
    }

    for moneda, ruta in archivos_json.items():
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
                logger.info(f"🧹 Archivo {moneda} eliminado correctamente: {ruta}")
            except Exception as e:
                logger.error(f"⚠️ No se pudo eliminar el archivo {moneda}: {e}")
        else:
            logger.info(f"ℹ️ No existe el archivo {moneda}, no es necesario eliminarlo.")