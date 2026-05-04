"""
app/routes/people.py — Rutas del directorio de personas.
Responsabilidad: Listado de académicos y perfiles individuales.
"""

import logging
from flask import Blueprint, render_template, abort
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

people_bp = Blueprint('people', __name__)


@people_bp.route('/')
def index():
    """Directorio de académicos."""
    from app.helpers import get_team
    team = get_team()
    logger.info(f"Directorio de académicos renderizado. Total: {len(team)}.")
    return render_template('pages/people.html',
                           team=team,
                           page_title='Académicos')


@people_bp.route('/<slug>')
def detail(slug):
    """Perfil individual de un académico."""
    from app.helpers import get_member_by_slug
    person = get_member_by_slug(slug)
    if person is None:
        logger.warning(f"Académico no encontrado: slug='{slug}'")
        abort(404)
    logger.info(f"Perfil renderizado: '{person['name']}'.")
    return render_template('pages/person_detail.html',
                           person=person,
                           page_title=person['name'])


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
