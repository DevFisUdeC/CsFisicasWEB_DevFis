"""
app/helpers.py — Funciones auxiliares compartidas por los blueprints.
Responsabilidad: Carga de datos JSON y utilidades comunes.
"""

import json
import os

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_cache = {}


def load_json(filename):
    """Carga un archivo JSON desde app/data/ con cache en memoria."""
    if filename in _cache:
        return _cache[filename]

    filepath = os.path.join(_DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _cache[filename] = data
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def clear_cache():
    """Limpia el cache de datos (útil en desarrollo)."""
    _cache.clear()


def get_team():
    """Retorna la lista de académicos."""
    return load_json('team.json')


def get_research_lines():
    """Retorna las líneas de investigación."""
    return load_json('research.json')


def get_programs():
    """Retorna los programas académicos."""
    return load_json('programs.json')


def get_news():
    """Retorna las noticias."""
    return load_json('news.json')


def get_config():
    """Retorna la configuración del sitio."""
    return load_json('config.json')
