"""
config.py — Configuración de la aplicación Flask.
Responsabilidad: Definir settings por entorno (dev, prod, test).
"""

import os


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

class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción (Vercel)."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuración para testing."""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
