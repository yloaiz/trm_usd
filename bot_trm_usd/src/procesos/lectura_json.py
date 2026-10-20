from bot_trm_usd.src.servicio_esb.get_token import get_token
from bot_trm_usd.src.config.logger_config import logger
from datetime import datetime
import requests
import json
import os
import time

url = os.getenv("URL_SERVICIO_TRM")

def lecturas_y_envio_datos_json():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 🔹 Carpeta donde está el JSON
    carpeta_descargas = os.path.join(os.getcwd(), "descargas")
    archivo_json = os.path.join(carpeta_descargas, "moneda_cambio_usd.json")

    # 🔹 Verificamos que exista
    if not os.path.exists(archivo_json):
        logger.info(f"⚠️ Archivo {archivo_json} no encontrado.")
        return

    # 🔹 Leemos el JSON
    with open(archivo_json, "r", encoding="utf-8") as file:
        datos = json.load(file)

    logger.info(f"\n📘 Procesando archivo {archivo_json}...\n")

    # ✅ Esperamos que el JSON tenga una sola clave-valor (ej: {"usd": "4132.50"})
    if not isinstance(datos, dict) or len(datos) == 0:
        logger.info("⚠️ El archivo JSON no tiene un formato válido o está vacío.")
        return

    # 🔹 Tomamos el primer (y único) elemento
    nombre_moneda, valor_cambio = next(iter(datos.items()))

    # 🔹 Homologación de código (si la clave no está en mayúscula)
    codigo_moneda = "USD" if nombre_moneda.lower() == "usd" else nombre_moneda.upper()

    payload = {
        "codigo_moneda": codigo_moneda,
        "trm": str(valor_cambio).replace('.', ''),  # Limpieza de separadores
        "fecha": str(datetime.today().date()),
        "tipo_cambio": "COP"
    }

    # 🔹 Mostrar lo que se enviará
    logger.info("➡️ Datos que se enviarían:")
    logger.info(payload)
    logger.info("-" * 60)

    # 🔹 Enviar a la API
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            logger.info(f"✅ Enviado {codigo_moneda} correctamente.")
        else:
            logger.error(f"❌ Error {response.status_code} enviando {codigo_moneda}: {response.text}")
    except Exception as e:
        logger.error(f"⚠️ Error enviando {codigo_moneda}: {e}")


    