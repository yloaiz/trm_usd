import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

import bot_trm_usd.src.correo.config_correo as config_correo
from bot_trm_usd.src.config.logger_config import logger


# Carpeta donde esta el archivo con el cuerpo del correo
base_path = os.path.abspath("descargas")

def leer_cuerpo_desde_json(nombre_archivo="moneda_cambio_usd.json"):
    """Lee el contenido del archivo .json que estará en Descagas"""
    ruta_archivo = os.path.join(base_path, nombre_archivo)
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return f.read()

def enviar_correo_notificacion_exitosa(destinatario, asunto):
    """Construye y envía el correo usando el cuerpo desde el txt"""
    datos = leer_cuerpo_desde_json()
    cuerpo = f"Estimados,\n\nConfirmo la actualizacion de TRM para el cambio de USD a Moneda local el dia de hoy:\n\n📊Datos en COP:\n" + datos + f"\n\nSaludos cordiales,\nAutomatización Maaji🤖"

    for email in destinatario:
        
        msg = MIMEMultipart()
        msg["From"] = config_correo.smtp_username
        msg["To"] = email
        msg["Subject"] = asunto
        # Cuerpo del correo
        msg.attach(MIMEText(cuerpo, "plain"))
        # Enviar
        with smtplib.SMTP(config_correo.smtp_server, config_correo.smtp_port) as server:
            server.starttls()
            server.login(config_correo.smtp_username, config_correo.smtp_password)
            server.sendmail(config_correo.smtp_username, email, msg.as_string())

        logger.info(f"Correo enviado a {email}")

def enviar_correo_notificacion_fallido(destinatario, asunto, cuerpo):
    """Construye y envía el correo usando el cuerpo desde el txt"""

    for email in destinatario:
        
        msg = MIMEMultipart()
        msg["From"] = config_correo.smtp_username
        msg["To"] = email
        msg["Subject"] = asunto
        # Cuerpo del correo
        msg.attach(MIMEText(cuerpo, "plain"))
        # Enviar
        with smtplib.SMTP(config_correo.smtp_server, config_correo.smtp_port) as server:
            server.starttls()
            server.login(config_correo.smtp_username, config_correo.smtp_password)
            server.sendmail(config_correo.smtp_username, email, msg.as_string())

        logger.info(f"Correo enviado a {email}")