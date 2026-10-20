
import base64
import os
from dotenv import load_dotenv

load_dotenv()

usuario_email = os.getenv("EMAIL_USER")
contraseña_email = os.getenv("EMAIL_PASSWORD")

#ENCRIPTACIÓN DE CONTRASEÑA EN BASE64
encode = contraseña_email
data = base64.b64decode(encode)
#TRANSOFMACIÓN DE INFORMACIÓN EN FORMATO UTF-8
password = data.decode('utf-8')

# 📌 Configuración SMTP - CONFIGURACIÓN DEL SERVIDOR
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587
smtp_username = usuario_email
smtp_password = password

CORREOS_PRUEBA = True  # Cambiar a False para enviar a todos los destinatarios
if CORREOS_PRUEBA:
    destinatario_correo = ['dtrivino@maaji.co','yloaiza@maaji.co']
else:
    destinatario_correo = ['dtrivino@maaji.co','ameneses@maaji.co']

asunto_correo = 'ACTUALIZACION TRM CAMBIO DE USD a COP - AUTOMATIZACIÓN'

# Cuerpo del correo para notificación de fallo en el proceso
cuerpo_proceso_fallido = "Estimados,\n\nHa ocurrido un error durante el proceso de actualización de TRM de USD a Moneda local el día de hoy. Por favor, revisar el sistema.\n\nSaludos cordiales,\n\nAutomatización Maaji🤖"