"""
app/routes/people.py — Rutas del directorio de personas.
Responsabilidad: Listado de académicos y perfiles individuales.
"""

from flask import Blueprint, render_template, abort
from app.helpers import get_team

people_bp = Blueprint('people', __name__)


@people_bp.route('/')
def index():
    """Directorio de académicos."""
    team = get_team()
    return render_template('pages/people.html',
                           team=team,
                           page_title='Académicos')


@people_bp.route('/<slug>')
def detail(slug):
    """Perfil individual de un académico."""
    team = get_team()
    person = next((p for p in team if p['slug'] == slug), None)
    if person is None:
        abort(404)
    return render_template('pages/person_detail.html',
                           person=person,
                           page_title=person['name'])
