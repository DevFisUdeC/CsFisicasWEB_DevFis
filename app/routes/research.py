"""
app/routes/research.py — Rutas de investigación.
Responsabilidad: Líneas de investigación, Publicaciones, Laboratorios.
"""

from flask import Blueprint, render_template
from app.helpers import get_research_lines

research_bp = Blueprint('research', __name__)


@research_bp.route('/')
def index():
    """Página principal de investigación — Líneas."""
    lines = get_research_lines()
    return render_template('pages/research.html',
                           research_lines=lines,
                           page_title='Investigación')


@research_bp.route('/publications')
def publications():
    """Página de publicaciones científicas."""
    return render_template('pages/publications.html',
                           page_title='Publicaciones')


@research_bp.route('/labs')
def labs():
    """Página de laboratorios."""
    return render_template('pages/labs.html',
                           page_title='Laboratorios')
