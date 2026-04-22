"""
config.py — Configuración de la aplicación Flask.
Responsabilidad: Definir settings por entorno (dev, prod, test).
"""

import os
from datetime import timedelta


class Config:
    """Configuración base compartida por todos los entornos."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-cambiar-en-produccion')
    SITE_NAME = 'Departamento de Física'
    SITE_SUBTITLE = 'Universidad de Concepción'
    SITE_URL = 'https://fisica.udec.cl'
    CONTACT_EMAIL = 'depfisica@udec.cl'
    CONTACT_PHONE = '+56 41 220 4334'
    CONTACT_ADDRESS = 'Avda. Esteban Iturra s/n, Barrio Universitario, Concepción, Chile'


    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin')
    ADMIN_PASS_HASH = os.environ.get('ADMIN_PASS_HASH', '')
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
    SUPABASE_BUCKET = os.environ.get('SUPABASE_BUCKET', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', str(10 * 1024 * 1024)))
    MAX_UPLOAD_FILE_SIZE = int(os.environ.get('MAX_UPLOAD_FILE_SIZE', str(5 * 1024 * 1024)))
    MAX_UPLOAD_FILES = int(os.environ.get('MAX_UPLOAD_FILES', '10'))
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuración para producción (Vercel)."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Configuración para testing."""
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
