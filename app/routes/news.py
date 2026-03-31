"""
app/routes/news.py — Rutas de noticias.
Responsabilidad: Listado de noticias y vista de noticia individual.
"""

from flask import Blueprint, render_template, abort
from app.helpers import get_news

news_bp = Blueprint('news', __name__)


@news_bp.route('/')
def index():
    """Listado de noticias."""
    news = get_news()
    return render_template('pages/news.html',
                           news=news,
                           page_title='Noticias')


@news_bp.route('/<slug>')
def detail(slug):
    """Vista de una noticia individual."""
    news = get_news()
    article = next((n for n in news if n['slug'] == slug), None)
    if article is None:
        abort(404)
    return render_template('pages/news_detail.html',
                           article=article,
                           page_title=article['title'])
