"""
app/routes/academics.py — Rutas académicas.
Responsabilidad: Pregrado, Postgrado, Malla Curricular.
"""

import logging
from pathlib import Path
from flask import Blueprint, render_template, send_from_directory, abort
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

academics_bp = Blueprint('academics', __name__)
DOCS_IMGS_DIR = Path(__file__).resolve().parents[2] / 'Docs' / 'Imgs'


@academics_bp.route('/undergraduate')
def undergraduate():
    """Página de pregrado — Ciencias Físicas."""
    from app.helpers import get_programs, get_page_hero_settings
    programs = get_programs()
    undergrad = programs.get('undergraduate', {})
    page_hero = get_page_hero_settings('undergraduate')
    logger.info("Página de pregrado renderizada.")
    return render_template('pages/undergraduate.html',
                           page_hero=page_hero,
                           program=undergrad,
                           page_title='Pregrado — Ciencias Físicas')


@academics_bp.route('/assets/malla-ciencias-fisicas.jpg')
def curriculum_image():
    """Sirve la malla curricular oficial desde Docs/Imgs."""
    filename = 'Ciencias-Fisicas_malla.jpg'
    img_path = DOCS_IMGS_DIR / filename
    if not img_path.exists():
        logger.error("No se encontró malla curricular en ruta esperada: %s", img_path)
        abort(404)
    # Recurso prácticamente estático: cache largo para mejorar entrega en producción.
    return send_from_directory(DOCS_IMGS_DIR, filename, max_age=31536000)


@academics_bp.route('/graduate')
def graduate():
    """Página de postgrado — Magíster y Doctorado."""
    from app.helpers import get_programs, get_page_hero_settings
    programs = get_programs()
    grad_programs = programs.get('graduate', [])
    page_hero = get_page_hero_settings('graduate')
    logger.info(f"Página de postgrado renderizada. Programas: {len(grad_programs)}.")
    return render_template('pages/graduate.html',
                           page_hero=page_hero,
                           programs=grad_programs,
                           page_title='Postgrado')


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)


