import json
import requests
from dotenv import load_dotenv
import os
import urllib3

load_dotenv()

url_banrep = os.getenv("URL_BANCO_REP")

def servicio_datos_banrep():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()

    payload = json.dumps({
        "idIndicador": 11,
        "menu": "1.1",
        "descripcion": "Tasa de cambio del peso colombiano, Tasa Representativa del Mercado (TRM)",
        "datosIndicador": {
            "listaMenu": [],
            "mostrarFormCorreoRecurrente": False,
            "listaIndicadorAgrupado": [],
            "isRecurrente": False
        }
    })

    data_usd = session.post(url_banrep, payload, verify=False).json()[0]["datosIndicador"]["valor"]

    return data_usd