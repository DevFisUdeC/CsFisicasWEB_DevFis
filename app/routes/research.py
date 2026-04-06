"""
app/routes/research.py — Rutas de investigación.
Responsabilidad: Líneas de investigación, Publicaciones, Laboratorios.
"""

import logging
from flask import Blueprint, render_template

logger = logging.getLogger(__name__)

research_bp = Blueprint('research', __name__)


@research_bp.route('/')
def index():
    """Página principal de investigación — Líneas."""
    from app.helpers import get_research_lines
    lines = get_research_lines()
    logger.info(f"Líneas de investigación renderizadas. Total: {len(lines)}.")
    return render_template('pages/research.html',
                           research_lines=lines,
                           page_title='Investigación')


@research_bp.route('/publications')
def publications():
    """Página de publicaciones científicas."""
    logger.info("Página de publicaciones renderizada.")
    return render_template('pages/publications.html',
                           page_title='Publicaciones')


@research_bp.route('/labs')
def labs():
    """Página de laboratorios."""
    logger.info("Página de laboratorios renderizada.")
    return render_template('pages/labs.html',
                           page_title='Laboratorios')
