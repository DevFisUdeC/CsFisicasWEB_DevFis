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

    _register_blueprints(app)
    _register_context_processors(app)
    _register_error_handlers(app)

    return app


def _register_blueprints(app):
    """Registra todos los blueprints de la aplicación."""
    from app.routes.main import main_bp
    from app.routes.academics import academics_bp
    from app.routes.research import research_bp
    from app.routes.people import people_bp
    from app.routes.news import news_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(academics_bp, url_prefix='/academics')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(people_bp, url_prefix='/people')
    app.register_blueprint(news_bp, url_prefix='/news')


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


def _get_nav_items():
    """Estructura de navegación del sitio."""
    return [
        {
            'label': 'Inicio',
            'url': '/',
            'children': [],
        },
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
                {'label': 'Malla Curricular', 'url': '/academics/curriculum'},
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
