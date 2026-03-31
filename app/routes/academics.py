"""
app/routes/academics.py — Rutas académicas.
Responsabilidad: Pregrado, Postgrado, Malla Curricular.
"""

from flask import Blueprint, render_template
from app.helpers import get_programs

academics_bp = Blueprint('academics', __name__)


@academics_bp.route('/undergraduate')
def undergraduate():
    """Página de pregrado — Ciencias Físicas."""
    programs = get_programs()
    undergrad = programs.get('undergraduate', {})
    return render_template('pages/undergraduate.html',
                           program=undergrad,
                           page_title='Pregrado — Ciencias Físicas')


@academics_bp.route('/graduate')
def graduate():
    """Página de postgrado — Magíster y Doctorado."""
    programs = get_programs()
    grad_programs = programs.get('graduate', [])
    return render_template('pages/graduate.html',
                           programs=grad_programs,
                           page_title='Postgrado')


@academics_bp.route('/curriculum')
def curriculum():
    """Malla curricular interactiva."""
    programs = get_programs()
    undergrad = programs.get('undergraduate', {})
    return render_template('pages/curriculum.html',
                           program=undergrad,
                           page_title='Malla Curricular')
