"""
app/routes/main.py — Rutas principales del sitio.
Responsabilidad: Home, About (Departamento), Contact.
"""

import json
import logging
from flask import Blueprint, render_template, request, current_app, Response
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Página de inicio."""
    from app.helpers import get_news, get_team, get_research_lines
    news = get_news()[:6]  # Últimas 6 noticias para home tipo portal
    team_count = len(get_team())
    research_count = len(get_research_lines())
    stats = {
        'academics': team_count,
        'students': '200+',
        'labs': 15,
        'publications': '300+',
    }
    logger.info("Página de inicio renderizada.")
    return render_template('pages/home.html',
                           news=news,
                           stats=stats,
                           page_title='Inicio')


@main_bp.route('/about')
def about():
    """Página sobre el departamento."""
    logger.info("Página del departamento renderizada.")
    return render_template('pages/about.html',
                           page_title='Departamento')


@main_bp.route('/contact')
def contact():
    """Página de contacto."""
    logger.info("Página de contacto renderizada.")
    return render_template('pages/contact.html',
                           page_title='Contacto')


@main_bp.route('/students')
def students():
    """Página de estudiantes: recursos académicos y documentos."""
    logger.info("Página de estudiantes renderizada.")
    return render_template('pages/students.html',
                           page_title='Estudiantes')


@main_bp.route('/_trace/client-event', methods=['GET', 'POST'])
def trace_client_event():
    """Recibe trazas de frontend y las imprime en terminal en modo debug."""
    if not current_app.debug:
        return Response(status=204)

    payload = {}

    if request.method == 'POST':
        try:
            if request.is_json:
                payload = request.get_json(silent=True) or {}
            else:
                raw = request.get_data(cache=False, as_text=True) or '{}'
                payload = json.loads(raw)
        except Exception:
            payload = {}

    if not payload:
        payload = request.args.to_dict(flat=True)

    event = payload.get('event', 'unknown')
    path = payload.get('path', '')
    label = payload.get('label', '')
    href = payload.get('href', '')
    meta = payload.get('meta', '')
    level = str(payload.get('level', 'info')).lower()

    message = "CLIENT EVENT | event=%s | path=%s | label=%s | href=%s | meta=%s"
    args = (event, path, label, href, meta)
    if level == 'debug':
        logger.debug(message, *args)
    elif level == 'warning':
        logger.warning(message, *args)
    elif level == 'error':
        logger.error(message, *args)
    else:
        logger.info(
            message,
            *args,
        )

    return Response(status=204)


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
