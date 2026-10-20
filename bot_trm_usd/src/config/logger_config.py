#src/utils/logger_config.py

import logging
import traceback
from bot_trm_usd.src.config.settings import path_base
import os


# ==========================================
# CONFIGURACIÓN DEL LOG
# ==========================================

LOG_FILE = os.path.join(path_base, "main.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
