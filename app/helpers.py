"""
app/helpers.py — Funciones auxiliares compartidas por los blueprints.
Responsabilidad: CRUD de datos vía Supabase (news, team), Storage
para imágenes, y carga de datos estáticos (JSON) para research/programs.
"""

import json
import logging
import os
import time
import imghdr

from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_cache = {}


# ═══════════════════════════════════════════════════════════════════════════════
#   Datos estáticos (JSON) — research, programs
# ═══════════════════════════════════════════════════════════════════════════════

def load_json(filename):
    """Carga un archivo JSON desde app/data/ con cache en memoria."""
    if filename in _cache:
        return _cache[filename]
    filepath = os.path.join(_DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _cache[filename] = data
            logger.debug(f"JSON cargado exitosamente: {filename}")
            return data
    except FileNotFoundError:
        logger.error(f"Archivo JSON no encontrado: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON {filename}: {e}")
        return {}


def get_research_lines():
    """Retorna las líneas de investigación (dato estático, JSON)."""
    return load_json('research.json')


def get_programs():
    """Retorna los programas académicos (dato estático, JSON)."""
    return load_json('programs.json')


# ═══════════════════════════════════════════════════════════════════════════════
#   NOTICIAS — Supabase table: public.news
# ═══════════════════════════════════════════════════════════════════════════════

def get_news():
    """Retorna todas las noticias ordenadas por fecha descendente."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='public').table('news').select('*').order('date', desc=True).execute()
        return resp.data or []
    except Exception as e:
        logger.error(f"Error al obtener noticias de Supabase: {e}")
        return []


def get_news_by_slug(slug):
    """Retorna una noticia por su slug, o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='public').table('news').select('*').eq('slug', slug).limit(1).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al obtener noticia '{slug}': {e}")
        return None


def create_news(data):
    """Inserta una noticia nueva. Retorna el registro insertado o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('news').insert(data).execute()
        logger.info(f"Noticia creada en Supabase: {data.get('title')}")
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al crear noticia: {e}")
        return None


def update_news(slug, data):
    """Actualiza una noticia por slug. Retorna el registro actualizado o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('news').update(data).eq('slug', slug).execute()
        logger.info(f"Noticia actualizada en Supabase: {slug}")
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al actualizar noticia '{slug}': {e}")
        return None


def delete_news_by_slug(slug):
    """Elimina una noticia por slug. Retorna True si se eliminó."""
    from app.database import get_supabase
    try:
        get_supabase(role='service').table('news').delete().eq('slug', slug).execute()
        logger.info(f"Noticia eliminada de Supabase: {slug}")
        return True
    except Exception as e:
        logger.error(f"Error al eliminar noticia '{slug}': {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   ACADÉMICOS — Supabase table: public.team_members
# ═══════════════════════════════════════════════════════════════════════════════

def get_team():
    """Retorna todos los académicos."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='public').table('team_members').select('*').order('name').execute()
        return resp.data or []
    except Exception as e:
        logger.error(f"Error al obtener equipo de Supabase: {e}")
        return []


def get_member_by_slug(slug):
    """Retorna un académico por su slug, o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='public').table('team_members').select('*').eq('slug', slug).limit(1).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al obtener académico '{slug}': {e}")
        return None


def create_team_member(data):
    """Inserta un académico nuevo. Retorna el registro o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('team_members').insert(data).execute()
        logger.info(f"Académico creado en Supabase: {data.get('name')}")
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al crear académico: {e}")
        return None


def update_team_member(slug, data):
    """Actualiza un académico por slug. Retorna el registro actualizado o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('team_members').update(data).eq('slug', slug).execute()
        logger.info(f"Académico actualizado en Supabase: {slug}")
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al actualizar académico '{slug}': {e}")
        return None


def delete_team_member_by_slug(slug):
    """Elimina un académico por slug. Retorna True si se eliminó."""
    from app.database import get_supabase
    try:
        get_supabase(role='service').table('team_members').delete().eq('slug', slug).execute()
        logger.info(f"Académico eliminado de Supabase: {slug}")
        return True
    except Exception as e:
        logger.error(f"Error al eliminar académico '{slug}': {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   IMÁGENES — Supabase Storage bucket: uploads
# ═══════════════════════════════════════════════════════════════════════════════

def _get_storage_url(bucket, filename):
    """Construye la URL pública de un archivo en Supabase Storage."""
    from app.database import get_supabase
    resp = get_supabase(role='service').storage.from_(bucket).get_public_url(filename)
    return resp


def upload_to_storage(file, bucket='uploads', allowed_extensions=None):
    """Sube un archivo a Supabase Storage. Retorna la URL pública o None."""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
    if not file or file.filename == '':
        return None

    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        logger.warning(f"Extensión no permitida: {ext}")
        return None

    from flask import current_app
    from app.database import get_supabase
    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    content = file.read()
    max_size = current_app.config.get('MAX_UPLOAD_FILE_SIZE', 5 * 1024 * 1024)
    if len(content) > max_size:
        logger.warning(f"Archivo excede límite de tamaño ({len(content)} > {max_size} bytes).")
        return None
    detected = imghdr.what(None, h=content)
    allowed_detected = {'png', 'jpeg', 'webp', 'gif'}
    if detected not in allowed_detected:
        logger.warning(f"Contenido no válido de imagen detectado: {detected}")
        return None
    mime_map = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'webp': 'image/webp', 'gif': 'image/gif'}
    content_type = mime_map.get(ext, 'application/octet-stream')

    try:
        get_supabase(role='service').storage.from_(bucket).upload(
            path=filename,
            file=content,
            file_options={"content-type": content_type},
        )
        public_url = _get_storage_url(bucket, filename)
        logger.info(f"Imagen subida a Storage: {filename}")
        return public_url
    except Exception as e:
        logger.error(f"Error al subir imagen a Storage: {e}")
        return None


def list_storage_files(bucket='uploads'):
    """Lista archivos del bucket de Supabase Storage."""
    from app.database import get_supabase
    try:
        files = get_supabase(role='service').storage.from_(bucket).list()
        result = []
        for f in files:
            if f.get('name', '').startswith('.'):
                continue
            name = f['name']
            url = _get_storage_url(bucket, name)
            size_kb = round(f.get('metadata', {}).get('size', 0) / 1024, 1) if f.get('metadata') else 0
            result.append({
                'filename': name,
                'url': url,
                'size_kb': size_kb,
            })
        return result
    except Exception as e:
        logger.error(f"Error al listar archivos de Storage: {e}")
        return []


def delete_from_storage(filename, bucket='uploads'):
    """Elimina un archivo de Supabase Storage."""
    from app.database import get_supabase
    try:
        get_supabase(role='service').storage.from_(bucket).remove([filename])
        logger.info(f"Imagen eliminada de Storage: {filename}")
        return True
    except Exception as e:
        logger.error(f"Error al eliminar imagen de Storage: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   UTILIDADES
# ═══════════════════════════════════════════════════════════════════════════════

def slugify(text):
    """Convierte texto a un slug URL-safe con soporte de tildes y ñ."""
    import re
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
