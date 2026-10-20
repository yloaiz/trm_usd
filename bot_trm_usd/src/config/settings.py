# src/config/settings.py
import os
import sys

def obtener_ruta_base():
    if getattr(sys, 'frozen', False):
        # Ejecutable (PyInstaller / Nuitka)
        base_path = os.path.dirname(sys.executable)
    else:
        # Proyecto en desarrollo
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )
    
    return base_path

path_base = obtener_ruta_base()
print(path_base)