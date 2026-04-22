"""
app/__init__.py — Application Factory de Flask.
Responsabilidad: Crear y configurar la instancia de la aplicación,
registrar blueprints y context processors.
"""

from flask import Flask
from config import config


def create_app(config_name='default'):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    _init_extensions(app)
    _register_blueprints(app)
    _register_context_processors(app)
    _register_error_handlers(app)
    _register_security_headers(app)

    return app

def _init_extensions(app):
    """Inicializa extensiones como Supabase, CSRF y rate limiter."""
    from app.database import init_supabase
    from flask_wtf.csrf import CSRFProtect
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    init_supabase(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    limiter_storage = app.config.get('RATELIMIT_STORAGE_URI', 'memory://')
    limiter = Limiter(get_remote_address, app=app, default_limits=[], storage_uri=limiter_storage)
    app.extensions['limiter'] = limiter

def _register_blueprints(app):
    """Registra todos los blueprints de la aplicación."""
    from app.routes.main import main_bp
    from app.routes.academics import academics_bp
    from app.routes.research import research_bp
    from app.routes.people import people_bp
    from app.routes.news import news_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(academics_bp, url_prefix='/academics')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    limiter = app.extensions.get('limiter')
    if limiter:
        limiter.limit("10/minute")(app.view_functions['admin.login'])


def _register_context_processors(app):
    """Variables disponibles en todos los templates."""
    @app.context_processor
    def inject_site_config():
        return {
            'site_name': app.config.get('SITE_NAME', 'Departamento de Física'),
            'site_subtitle': app.config.get('SITE_SUBTITLE', 'Universidad de Concepción'),
            'contact_email': app.config.get('CONTACT_EMAIL', ''),
            'contact_phone': app.config.get('CONTACT_PHONE', ''),
            'contact_address': app.config.get('CONTACT_ADDRESS', ''),
            'nav_items': _get_nav_items(),
        }


def _register_error_handlers(app):
    """Registra manejadores de errores HTTP."""
    from flask import render_template

    @app.errorhandler(404)
    def not_found(error):
        return render_template('pages/errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('pages/errors/500.html'), 500


def _register_security_headers(app):
    """Aplica cabeceras de seguridad en respuestas HTTP."""
    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'DENY')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.headers.setdefault('Content-Security-Policy', "default-src 'self'; img-src 'self' https: data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; object-src 'none'")
        if not app.debug:
            response.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        return response


def _get_nav_items():
    """Estructura de navegación del sitio."""
    return [
        {
            'label': 'Departamento',
            'url': '/about',
            'children': [
                {'label': 'Historia', 'url': '/about#historia'},
                {'label': 'Misión y Visión', 'url': '/about#mision'},
                {'label': 'Organigrama', 'url': '/about#organigrama'},
            ],
        },
        {
            'label': 'Académicos',
            'url': '/people',
            'children': [],
        },
        {
            'label': 'Pregrado',
            'url': '/academics/undergraduate',
            'children': [
                {'label': 'Ciencias Físicas', 'url': '/academics/undergraduate'},
                {'label': 'Malla Curricular', 'url': '/academics/undergraduate#malla-curricular'},
            ],
        },
        {
            'label': 'Postgrado',
            'url': '/academics/graduate',
            'children': [
                {'label': 'Magíster en Física', 'url': '/academics/graduate#magister'},
                {'label': 'Doctorado en Cs. Físicas', 'url': '/academics/graduate#doctorado'},
            ],
        },
        {
            'label': 'Investigación',
            'url': '/research',
            'children': [
                {'label': 'Líneas de Investigación', 'url': '/research'},
                {'label': 'Publicaciones', 'url': '/research/publications'},
                {'label': 'Laboratorios', 'url': '/research/labs'},
            ],
        },
        {
            'label': 'Noticias',
            'url': '/news',
            'children': [],
        },
        {
            'label': 'Contacto',
            'url': '/contact',
            'children': [],
        },
    ]
