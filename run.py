"""
run.py — Entry point para el servidor de desarrollo Flask.
Responsabilidad: Iniciar la aplicación con la configuración correcta.
"""

import logging
import os

from dotenv import load_dotenv
load_dotenv()

from app import create_app

APP_ENV = os.environ.get('APP_ENV', 'development').strip().lower()
if APP_ENV not in {'development', 'production', 'testing'}:
    APP_ENV = 'development'

app = create_app(APP_ENV)

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', str(app.config.get('DEBUG', False))).lower() in {'1', 'true', 'yes'}

    logger = logging.getLogger(__name__)
    logger.info("Iniciando servidor Flask...")
    logger.info("APP_ENV=%s | DEBUG=%s | HOST=%s | PORT=%s", APP_ENV, debug, host, port)
    logger.info(
        "Límites upload | MAX_CONTENT_LENGTH=%s MB | MAX_UPLOAD_FILE_SIZE=%s MB | MAX_HERO_UPLOAD_FILE_SIZE=%s MB",
        round((app.config.get('MAX_CONTENT_LENGTH', 0) or 0) / (1024 * 1024), 2),
        round((app.config.get('MAX_UPLOAD_FILE_SIZE', 0) or 0) / (1024 * 1024), 2),
        round((app.config.get('MAX_HERO_UPLOAD_FILE_SIZE', 0) or 0) / (1024 * 1024), 2),
    )

    app.run(host=host, port=port, debug=debug)
