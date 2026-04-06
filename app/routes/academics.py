"""
app/routes/academics.py — Rutas académicas.
Responsabilidad: Pregrado, Postgrado, Malla Curricular.
"""

import logging
from flask import Blueprint, render_template

logger = logging.getLogger(__name__)

academics_bp = Blueprint('academics', __name__)


@academics_bp.route('/undergraduate')
def undergraduate():
    """Página de pregrado — Ciencias Físicas."""
    from app.helpers import get_programs
    programs = get_programs()
    undergrad = programs.get('undergraduate', {})
    logger.info("Página de pregrado renderizada.")
    return render_template('pages/undergraduate.html',
                           program=undergrad,
                           page_title='Pregrado — Ciencias Físicas')


@academics_bp.route('/graduate')
def graduate():
    """Página de postgrado — Magíster y Doctorado."""
    from app.helpers import get_programs
    programs = get_programs()
    grad_programs = programs.get('graduate', [])
    logger.info(f"Página de postgrado renderizada. Programas: {len(grad_programs)}.")
    return render_template('pages/graduate.html',
                           programs=grad_programs,
                           page_title='Postgrado')


