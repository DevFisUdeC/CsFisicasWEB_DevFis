"""
app/routes/news.py — Rutas de noticias.
Responsabilidad: Listado de noticias y vista de noticia individual.
"""

import logging
from flask import Blueprint, render_template, abort
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

news_bp = Blueprint('news', __name__)


@news_bp.route('/')
def index():
    """Listado de noticias."""
    from app.helpers import get_news
    news = get_news()
    logger.info(f"Listado de noticias renderizado. Total: {len(news)}.")
    return render_template('pages/news.html',
                           news=news,
                           page_title='Noticias')


@news_bp.route('/<slug>')
def detail(slug):
    """Vista de una noticia individual."""
    from app.helpers import get_news_by_slug
    article = get_news_by_slug(slug)
    if article is None:
        logger.warning(f"Noticia no encontrada: slug='{slug}'")
        abort(404)
    logger.info(f"Detalle de noticia renderizado: '{article['title']}'.")
    return render_template('pages/news_detail.html',
                           article=article,
                           page_title=article['title'])


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
