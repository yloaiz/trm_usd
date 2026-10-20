import os
import json
from bot_trm_usd.src.config.logger_config import logger

def crear_json(tasa):
    # Estructura del JSON
    data = {"usd": tasa}

    ruta = os.path.abspath("descargas")
    # Asegurar que la carpeta exista
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        logger.info(f"📁 Carpeta creada: {ruta}")

    # Ruta completa del archivo JSON
    ruta_json = os.path.join(ruta, "moneda_cambio_usd.json")

    # Guardar en archivo JSON
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)