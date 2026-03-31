"""
app/routes/main.py — Rutas principales del sitio.
Responsabilidad: Home, About (Departamento), Contact.
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Página de inicio."""
    from app.helpers import get_news, get_team, get_research_lines
    news = get_news()[:3]  # Últimas 3 noticias
    team_count = len(get_team())
    research_count = len(get_research_lines())
    stats = {
        'academics': team_count,
        'students': '200+',
        'labs': 15,
        'publications': '300+',
    }
    return render_template('pages/home.html',
                           news=news,
                           stats=stats,
                           page_title='Inicio')


@main_bp.route('/about')
def about():
    """Página sobre el departamento."""
    return render_template('pages/about.html',
                           page_title='Departamento')


@main_bp.route('/contact')
def contact():
    """Página de contacto."""
    return render_template('pages/contact.html',
                           page_title='Contacto')
