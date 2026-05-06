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
from urllib.parse import unquote
from io import BytesIO
from pathlib import Path

from werkzeug.utils import secure_filename
from PIL import Image
from PIL import ImageFilter
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_cache = {}
_SITE_SETTINGS_FILE = Path(_DATA_DIR) / 'site_settings.json'
_UI_SETTINGS_FILE = Path(_DATA_DIR) / 'ui_settings.json'
_STATIC_DIR = Path(__file__).resolve().parent / 'static'
_PAGE_HERO_CONTEXTS = {
    'home': {
        'label': 'Home',
        'final_image_rel': 'img/hero/home-hero.webp',
        'original_image_rel': 'img/hero/home-hero-original.webp',
    },
    'about': {
        'label': 'Departamento',
        'final_image_rel': 'img/hero/about-hero.webp',
        'original_image_rel': 'img/hero/about-hero-original.webp',
    },
    'people': {
        'label': 'Académicos',
        'final_image_rel': 'img/hero/people-hero.webp',
        'original_image_rel': 'img/hero/people-hero-original.webp',
    },
    'undergraduate': {
        'label': 'Pregrado',
        'final_image_rel': 'img/hero/undergraduate-hero.webp',
        'original_image_rel': 'img/hero/undergraduate-hero-original.webp',
    },
    'graduate': {
        'label': 'Postgrado',
        'final_image_rel': 'img/hero/graduate-hero.webp',
        'original_image_rel': 'img/hero/graduate-hero-original.webp',
    },
    'students': {
        'label': 'Estudiantes',
        'final_image_rel': 'img/hero/students-hero.webp',
        'original_image_rel': 'img/hero/students-hero-original.webp',
    },
    'research': {
        'label': 'Investigación',
        'final_image_rel': 'img/hero/research-hero.webp',
        'original_image_rel': 'img/hero/research-hero-original.webp',
    },
    'news': {
        'label': 'Noticias',
        'final_image_rel': 'img/hero/news-hero.webp',
        'original_image_rel': 'img/hero/news-hero-original.webp',
    },
    'contact': {
        'label': 'Contacto',
        'final_image_rel': 'img/hero/contact-hero.webp',
        'original_image_rel': 'img/hero/contact-hero-original.webp',
    },
}
_HERO_SETTINGS_STORAGE_OBJECT = 'hero/site-settings.json'
_HERO_STORAGE_PREFIX = 'hero'
_HERO_STORAGE_FILES_CACHE = {
    'fetched_at': 0.0,
    'files': set(),
}


def _serverless_read_only_fs_enabled():
    """Indica si se debe evitar persistencia local (ej. Vercel serverless)."""
    try:
        from flask import current_app
        return bool(current_app.config.get('SERVERLESS_READ_ONLY_FS', False))
    except RuntimeError:
        return False


def _is_read_only_fs_error(error):
    """Detecta error de filesystem solo lectura."""
    try:
        import errno
        if getattr(error, 'errno', None) == errno.EROFS:
            return True
    except Exception:
        pass
    return 'read-only file system' in str(error).lower()


def _default_ui_settings():
    """Parámetros UI centralizados para evitar hardcode en vistas/controles."""
    return {
        'navbar': {
            'udec_logo': {
                'desktop': {
                    'min': '60px',
                    'fluid': '6.7vw',
                    'max': '79px',
                    'max_width': '180px',
                },
                'tablet': {
                    'min': '54px',
                    'fluid': '6.6vw',
                    'max': '74px',
                    'max_width': '170px',
                },
                'mobile': {
                    'min': '64px',
                    'fluid': '17vw',
                    'max': '81px',
                    'max_width': '188px',
                },
            }
        },
        'buttons': {
            'touch_min_height': '44px',
        },
        'hero': {
            'position_min': 0,
            'position_max': 200,
            'default_position_x': 50,
            'default_position_y': 45,
            'zoom_min': 0.01,
            'zoom_max': 10.0,
            'zoom_step': 0.01,
            'default_zoom': 1.0,
            'crop_min': 0,
            'crop_max': 30,
            'overlay_min': 0.0,
            'overlay_max': 0.9,
            'overlay_step': 0.05,
            'default_overlay_opacity': 0.45,
            'layout': {
                'desktop': {
                    'padding_min': '3.8rem',
                    'padding_fluid': '6vw',
                    'padding_max': '5rem',
                    'subtitle_size': 'var(--font-size-lg)',
                    'subtitle_max_width': '700px',
                },
                'tablet': {
                    'padding_min': '2.4rem',
                    'padding_fluid': '10vw',
                    'padding_max': '3.5rem',
                    'min_height_min': '240px',
                    'min_height_fluid': '56vw',
                    'min_height_max': '360px',
                    'title_min': '1.95rem',
                    'title_fluid': '8vw',
                    'title_max': '2.55rem',
                    'subtitle_min': '1.02rem',
                    'subtitle_fluid': '4.6vw',
                    'subtitle_max': '1.2rem',
                    'compact_min_height_min': '210px',
                    'compact_min_height_fluid': '44vw',
                    'compact_min_height_max': '285px',
                    'compact_padding_top_min': '1.8rem',
                    'compact_padding_top_fluid': '7vw',
                    'compact_padding_top_max': '2.5rem',
                    'compact_padding_bottom_min': '1.25rem',
                    'compact_padding_bottom_fluid': '5.5vw',
                    'compact_padding_bottom_max': '2rem',
                    'compact_title_min': '1.8rem',
                    'compact_title_fluid': '7.1vw',
                    'compact_title_max': '2.25rem',
                    'compact_subtitle_min': '0.98rem',
                    'compact_subtitle_fluid': '4.1vw',
                    'compact_subtitle_max': '1.12rem',
                },
                'mobile': {
                    'min_height_min': '225px',
                    'min_height_fluid': '60vw',
                    'min_height_max': '320px',
                    'padding_min': '2rem',
                    'padding_fluid': '8vw',
                    'padding_max': '2.8rem',
                    'title_min': '1.85rem',
                    'title_fluid': '9.2vw',
                    'title_max': '2.2rem',
                    'subtitle_size': '1.05rem',
                    'compact_min_height_min': '190px',
                    'compact_min_height_fluid': '50vw',
                    'compact_min_height_max': '250px',
                    'compact_padding_top_min': '1.5rem',
                    'compact_padding_top_fluid': '6.5vw',
                    'compact_padding_top_max': '2.1rem',
                    'compact_padding_bottom_min': '1rem',
                    'compact_padding_bottom_fluid': '5vw',
                    'compact_padding_bottom_max': '1.6rem',
                    'compact_title_min': '1.6rem',
                    'compact_title_fluid': '6.9vw',
                    'compact_title_max': '2rem',
                    'compact_subtitle_min': '0.92rem',
                    'compact_subtitle_fluid': '3.8vw',
                    'compact_subtitle_max': '1.02rem',
                },
            },
            'mobile_pan': {
                'breakpoint': 768,
                'wide_ratio': 1.6,
                'medium_ratio': 1.2,
                'wide_sweep': 44,
                'medium_sweep': 30,
                'narrow_sweep': 18,
                'duration_wide_s': 22,
                'duration_medium_s': 24,
                'duration_narrow_s': 26,
            },
        }
    }


def _deep_merge_dict(base, override):
    """Merge recursivo simple para diccionarios."""
    merged = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def get_ui_settings():
    """Carga configuración UI editable desde app/data/ui_settings.json."""
    settings = _default_ui_settings()
    if not _UI_SETTINGS_FILE.exists():
        return settings
    try:
        with _UI_SETTINGS_FILE.open('r', encoding='utf-8') as f:
            disk = json.load(f)
        if isinstance(disk, dict):
            settings = _deep_merge_dict(settings, disk)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"No se pudo cargar ui_settings.json: {e}")
    return settings


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


def _default_site_settings():
    """Configuración por defecto editable por panel admin."""
    ui_hero = get_ui_settings().get('hero', {})
    default_x = int(ui_hero.get('default_position_x', 50))
    default_y = int(ui_hero.get('default_position_y', 45))
    default_zoom = float(ui_hero.get('default_zoom', 1.0))
    default_overlay = float(ui_hero.get('default_overlay_opacity', 0.45))
    page_heroes = {}
    for key, cfg in _PAGE_HERO_CONTEXTS.items():
        page_heroes[key] = {
            'enabled': False,
            'image': cfg['final_image_rel'],
            'position_x': default_x,
            'position_y': default_y,
            'zoom': default_zoom,
            'crop_left': 0,
            'crop_right': 0,
            'crop_top': 0,
            'crop_bottom': 0,
            'overlay_opacity': default_overlay,
            'blur_enabled': False,
        }
    return {'page_heroes': page_heroes}


def _load_site_settings():
    """Carga configuración de sitio desde archivo JSON local."""
    settings = _default_site_settings()
    disk_settings = None
    prefer_storage = _serverless_read_only_fs_enabled() and _hero_settings_storage_enabled()

    if prefer_storage:
        disk_settings = _load_site_settings_from_storage()

    if disk_settings is None and _SITE_SETTINGS_FILE.exists():
        try:
            with _SITE_SETTINGS_FILE.open('r', encoding='utf-8') as f:
                disk_settings = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"No se pudo cargar site_settings.json local: {e}")

    # Fallback remoto cuando no hay configuración local válida.
    if disk_settings is None and not prefer_storage:
        disk_settings = _load_site_settings_from_storage()

    if isinstance(disk_settings, dict):
        # Compatibilidad con estructura antigua (home_hero al nivel raíz).
        if 'home_hero' in disk_settings and isinstance(disk_settings.get('home_hero'), dict):
            disk_settings.setdefault('page_heroes', {})
            disk_settings['page_heroes'].setdefault('home', {})
            disk_settings['page_heroes']['home'].update(disk_settings.get('home_hero', {}))
            disk_settings.pop('home_hero', None)

        for key, value in disk_settings.items():
            if key == 'page_heroes' and isinstance(value, dict):
                settings['page_heroes'].update(value)
            else:
                settings[key] = value
    return settings


def _save_site_settings(settings):
    """Guarda configuración de sitio en archivo JSON local."""
    stored_remote = _save_site_settings_to_storage(settings)
    if _serverless_read_only_fs_enabled():
        return stored_remote
    try:
        _SITE_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _SITE_SETTINGS_FILE.open('w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        if _is_read_only_fs_error(e):
            logger.info("Persistencia local deshabilitada (filesystem solo lectura). Se usa Storage.")
        else:
            logger.warning(f"No se pudo guardar site_settings.json local: {e}")
        return stored_remote


def _hero_storage_enabled():
    """Indica si portadas deben persistirse en Supabase Storage."""
    try:
        from flask import current_app
        return bool(current_app.config.get('HERO_USE_SUPABASE_STORAGE', True))
    except RuntimeError:
        return True


def _hero_settings_storage_enabled():
    """Controla si los settings JSON se leen/escriben en Storage."""
    try:
        from flask import current_app
        return bool(current_app.config.get('HERO_SETTINGS_USE_SUPABASE_STORAGE', False))
    except RuntimeError:
        return False


def _hero_storage_bucket():
    """Bucket usado para configuraciones/imagenes hero."""
    from flask import current_app
    return current_app.config.get('SUPABASE_BUCKET', 'uploads')


def _hero_storage_prefix():
    """Prefijo de objetos hero en bucket."""
    from flask import current_app
    prefix = str(current_app.config.get('HERO_STORAGE_PREFIX', _HERO_STORAGE_PREFIX)).strip('/')
    return prefix or _HERO_STORAGE_PREFIX


def _hero_settings_storage_object():
    """Path del JSON de settings hero en Storage."""
    return f"{_hero_storage_prefix()}/site-settings.json"


def _upload_storage_bytes(path, content, content_type='application/octet-stream'):
    """Sube bytes a Storage con upsert."""
    if not _hero_storage_enabled():
        return False
    from app.database import get_supabase
    try:
        get_supabase(role='service').storage.from_(_hero_storage_bucket()).upload(
            path=path,
            file=content,
            file_options={"content-type": content_type},
        )
        return True
    except Exception as e:
        err_text = str(e).lower()
        # Si ya existe, se reemplaza explícitamente (upload->remove->upload)
        if 'duplicate' in err_text or 'already exists' in err_text:
            try:
                get_supabase(role='service').storage.from_(_hero_storage_bucket()).remove([path])
                get_supabase(role='service').storage.from_(_hero_storage_bucket()).upload(
                    path=path,
                    file=content,
                    file_options={"content-type": content_type},
                )
                return True
            except Exception as inner_e:
                logger.error(f"No se pudo reemplazar objeto en Storage ({path}): {inner_e}")
                return False
        logger.error(f"No se pudo subir objeto a Storage ({path}): {e}")
        return False


def _convert_image_bytes(content, target_format='JPEG', quality=88):
    """Convierte bytes de imagen a otro formato."""
    with Image.open(BytesIO(content)) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        elif img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        out = BytesIO()
        save_kwargs = {}
        if target_format.upper() in {'JPEG', 'WEBP'}:
            save_kwargs['quality'] = quality
        img.save(out, format=target_format.upper(), **save_kwargs)
        return out.getvalue()


def _upload_storage_image_bytes(path, image_bytes):
    """Sube imagen a Storage con fallback de mimes/formatos."""
    candidates = []
    candidates.append((image_bytes, 'image/webp'))
    try:
        candidates.append((_convert_image_bytes(image_bytes, target_format='JPEG', quality=88), 'image/jpeg'))
    except Exception as e:
        logger.warning(f"No se pudo generar fallback JPEG para Storage ({path}): {e}")
    try:
        candidates.append((_convert_image_bytes(image_bytes, target_format='PNG', quality=92), 'image/png'))
    except Exception as e:
        logger.warning(f"No se pudo generar fallback PNG para Storage ({path}): {e}")

    for payload, mime in candidates:
        if _upload_storage_bytes(path, payload, content_type=mime):
            if mime != 'image/webp':
                logger.warning("Imagen hero guardada con mime fallback: %s", mime)
            return True
    return False


def _download_storage_bytes(path):
    """Descarga bytes desde Storage."""
    if not _hero_storage_enabled():
        return None
    from app.database import get_supabase
    try:
        data = get_supabase(role='service').storage.from_(_hero_storage_bucket()).download(path)
        if isinstance(data, bytes):
            return data
        if hasattr(data, 'read'):
            return data.read()
    except Exception as e:
        # En primera carga es normal que no exista aún.
        if 'not_found' in str(e).lower():
            logger.debug(f"Objeto hero aún no existe en Storage ({path}).")
        else:
            logger.warning(f"No se pudo descargar objeto de Storage ({path}): {e}")
    return None


def _list_hero_storage_files():
    """Lista archivos hero en Storage con caché corta."""
    if not _hero_storage_enabled():
        return set()
    now = time.time()
    if now - _HERO_STORAGE_FILES_CACHE['fetched_at'] < 20:
        return _HERO_STORAGE_FILES_CACHE['files']

    from app.database import get_supabase
    files = set()
    prefix = _hero_storage_prefix()
    try:
        listed = get_supabase(role='service').storage.from_(_hero_storage_bucket()).list(prefix)
        for item in listed or []:
            name = item.get('name')
            if name:
                files.add(f"{prefix}/{name}")
    except Exception as e:
        logger.warning(f"No se pudo listar objetos hero en Storage: {e}")

    _HERO_STORAGE_FILES_CACHE['fetched_at'] = now
    _HERO_STORAGE_FILES_CACHE['files'] = files
    return files


def _storage_object_exists(path):
    """Verifica existencia de un objeto hero en Storage."""
    return path in _list_hero_storage_files()


def _load_site_settings_from_storage():
    """Carga settings hero desde Storage cuando están disponibles."""
    if not (_hero_storage_enabled() and _hero_settings_storage_enabled()):
        return None
    raw = _download_storage_bytes(_hero_settings_storage_object())
    if not raw:
        return None
    try:
        payload = raw.decode('utf-8')
        data = json.loads(payload)
        return data if isinstance(data, dict) else None
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logger.error(f"No se pudo decodificar settings hero desde Storage: {e}")
        return None


def _save_site_settings_to_storage(settings):
    """Guarda settings hero como JSON en Storage."""
    if not (_hero_storage_enabled() and _hero_settings_storage_enabled()):
        return False
    try:
        data = json.dumps(settings, ensure_ascii=False, indent=2).encode('utf-8')
    except (TypeError, ValueError) as e:
        logger.error(f"No se pudo serializar settings hero: {e}")
        return False
    settings_path = _hero_settings_storage_object()
    ok = _upload_storage_bytes(
        settings_path,
        data,
        content_type='application/json',
    )
    if ok:
        # Fuerza recarga de cache de lista para reflejar nuevos objetos.
        _HERO_STORAGE_FILES_CACHE['fetched_at'] = 0.0
    else:
        logger.error(
            "No se pudo guardar settings hero en Storage con content-type application/json. "
            "Revisa los MIME permitidos del bucket y habilita application/json para %s.",
            settings_path,
        )
    return ok


def _normalize_home_hero_image(content, max_width=3200, quality=92):
    """Normaliza imagen original del hero y la exporta como WEBP."""
    with Image.open(BytesIO(content)) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        elif img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        width, height = img.size
        if width > max_width:
            ratio = max_width / float(width)
            new_size = (max_width, int(height * ratio))
            resampling = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
            img = img.resize(new_size, resampling)

        out = BytesIO()
        img.save(out, format='WEBP', quality=quality, method=6)
        return out.getvalue()


def _get_page_hero_paths(page_key):
    """Resuelve paths de imagen final/original para un contexto de portada."""
    context = _PAGE_HERO_CONTEXTS.get(page_key)
    if not context:
        raise KeyError(f"Contexto de hero no soportado: {page_key}")
    return {
        'label': context['label'],
        'final_rel': context['final_image_rel'],
        'original_rel': context['original_image_rel'],
        'final_abs': _STATIC_DIR / context['final_image_rel'],
        'original_abs': _STATIC_DIR / context['original_image_rel'],
        'storage_final': f"{_hero_storage_prefix()}/{page_key}-hero.webp",
        'storage_original': f"{_hero_storage_prefix()}/{page_key}-hero-original.webp",
    }


def get_page_hero_contexts():
    """Retorna contextos disponibles para configuración de portada."""
    return [{'key': key, 'label': cfg['label']} for key, cfg in _PAGE_HERO_CONTEXTS.items()]


def _build_page_hero_image_bytes(original_content, hero_settings, output_max_width=2200, quality=86, target_ratio=(1600 / 420)):
    """Genera bytes WEBP finales del hero aplicando recortes y zoom."""
    with Image.open(BytesIO(original_content)) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        crop_left = max(0, min(30, int(hero_settings.get('crop_left', 0))))
        crop_right = max(0, min(30, int(hero_settings.get('crop_right', 0))))
        crop_top = max(0, min(30, int(hero_settings.get('crop_top', 0))))
        crop_bottom = max(0, min(30, int(hero_settings.get('crop_bottom', 0))))

        # Evita recortes imposibles.
        if crop_left + crop_right >= 95:
            crop_right = max(0, 94 - crop_left)
        if crop_top + crop_bottom >= 95:
            crop_bottom = max(0, 94 - crop_top)

        x0 = int(width * (crop_left / 100.0))
        x1 = int(width * (1 - (crop_right / 100.0)))
        y0 = int(height * (crop_top / 100.0))
        y1 = int(height * (1 - (crop_bottom / 100.0)))
        x1 = max(x0 + 10, x1)
        y1 = max(y0 + 10, y1)
        img = img.crop((x0, y0, x1, y1))

        width, height = img.size
        ui_hero = get_ui_settings().get('hero', {})
        zoom_min = float(ui_hero.get('zoom_min', 0.01))
        zoom_max = float(ui_hero.get('zoom_max', 10.0))
        default_zoom = float(ui_hero.get('default_zoom', 1.0))
        pos_min = int(ui_hero.get('position_min', 0))
        pos_max = int(ui_hero.get('position_max', 200))
        default_x = int(ui_hero.get('default_position_x', 50))
        default_y = int(ui_hero.get('default_position_y', 45))

        zoom_factor = max(zoom_min, min(zoom_max, float(hero_settings.get('zoom', default_zoom))))
        focus_x = max(pos_min, min(pos_max, int(hero_settings.get('position_x', default_x))))
        focus_y = max(pos_min, min(pos_max, int(hero_settings.get('position_y', default_y))))
        range_span = max(1, pos_max - pos_min)
        focus_x_normalized = (focus_x - pos_min) / float(range_span)
        focus_y_normalized = (focus_y - pos_min) / float(range_span)
        out_w = min(output_max_width, max(10, width))
        out_h = max(10, int(out_w / target_ratio))
        resampling = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS

        cover_scale = max(out_w / float(width), out_h / float(height))
        scale = cover_scale * zoom_factor
        draw_w = max(1, int(width * scale))
        draw_h = max(1, int(height * scale))

        # Fondo base: versión cover desenfocada de la misma imagen.
        bg = img.copy()
        bg_scale = cover_scale
        bg_w = max(1, int(width * bg_scale))
        bg_h = max(1, int(height * bg_scale))
        bg = bg.resize((bg_w, bg_h), resampling)
        bg_left = (bg_w - out_w) // 2
        bg_top = (bg_h - out_h) // 2
        bg = bg.crop((bg_left, bg_top, bg_left + out_w, bg_top + out_h)).filter(ImageFilter.GaussianBlur(radius=16))

        # Capa principal ajustable por foco.
        fg = img.resize((draw_w, draw_h), resampling)
        if draw_w > out_w:
            fg_x = -int((draw_w - out_w) * focus_x_normalized)
        else:
            fg_x = (out_w - draw_w) // 2
        if draw_h > out_h:
            fg_y = -int((draw_h - out_h) * focus_y_normalized)
        else:
            fg_y = (out_h - draw_h) // 2

        composed = bg.copy()
        composed.paste(fg, (fg_x, fg_y))
        if bool(hero_settings.get('blur_enabled', False)):
            composed = composed.filter(ImageFilter.GaussianBlur(radius=8))

        out = BytesIO()
        composed.save(out, format='WEBP', quality=quality, method=6)
        return out.getvalue()


def _build_page_hero_from_original(page_key, hero_settings):
    """Genera imagen final hero en local y Storage (cuando esté habilitado)."""
    paths = _get_page_hero_paths(page_key)
    original_path = paths['original_abs']
    final_path = paths['final_abs']

    original_content = _download_storage_bytes(paths['storage_original'])
    if original_content is None and original_path.exists():
        original_content = original_path.read_bytes()

    if not original_content and final_path.exists():
        original_content = final_path.read_bytes()

    if not original_content:
        raise FileNotFoundError("No existe imagen original de portada.")

    final_bytes = _build_page_hero_image_bytes(original_content, hero_settings)

    if _hero_storage_enabled():
        if not _upload_storage_image_bytes(paths['storage_final'], final_bytes):
            raise RuntimeError("No se pudo guardar imagen final en Storage.")
        _HERO_STORAGE_FILES_CACHE['fetched_at'] = 0.0

    if _serverless_read_only_fs_enabled():
        return
    try:
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_bytes(final_bytes)
    except OSError as e:
        if not _hero_storage_enabled():
            raise
        if _is_read_only_fs_error(e):
            logger.info("Respaldo local de hero final omitido (filesystem solo lectura).")
        else:
            logger.warning(f"No se pudo guardar respaldo local de hero final: {e}")


def get_page_hero_settings(page_key):
    """Retorna configuración efectiva del hero para una página."""
    if page_key not in _PAGE_HERO_CONTEXTS:
        return None
    from flask import url_for
    paths = _get_page_hero_paths(page_key)
    settings = _load_site_settings()
    hero = settings.get('page_heroes', {}).get(page_key, {})
    ui_hero = get_ui_settings().get('hero', {})
    pos_min = int(ui_hero.get('position_min', 0))
    pos_max = int(ui_hero.get('position_max', 200))
    default_x = int(ui_hero.get('default_position_x', 50))
    default_y = int(ui_hero.get('default_position_y', 45))
    default_overlay = float(ui_hero.get('default_overlay_opacity', 0.45))
    local_exists = paths['final_abs'].exists()
    storage_exists = _storage_object_exists(paths['storage_final'])
    original_local_exists = paths['original_abs'].exists()
    original_storage_exists = _storage_object_exists(paths['storage_original'])
    image_exists = storage_exists or local_exists
    prefer_storage_assets = _serverless_read_only_fs_enabled() and _hero_storage_enabled()
    if prefer_storage_assets:
        if storage_exists:
            image_url = _get_storage_url(_hero_storage_bucket(), paths['storage_final'])
        elif local_exists:
            image_url = url_for('static', filename=paths['final_rel'])
        else:
            image_url = ''
        if original_storage_exists:
            original_image_url = _get_storage_url(_hero_storage_bucket(), paths['storage_original'])
        elif original_local_exists:
            original_image_url = url_for('static', filename=paths['original_rel'])
        else:
            original_image_url = ''
    else:
        if local_exists:
            image_url = url_for('static', filename=paths['final_rel'])
        elif storage_exists:
            image_url = _get_storage_url(_hero_storage_bucket(), paths['storage_final'])
        else:
            image_url = ''
        if original_local_exists:
            original_image_url = url_for('static', filename=paths['original_rel'])
        elif original_storage_exists:
            original_image_url = _get_storage_url(_hero_storage_bucket(), paths['storage_original'])
        else:
            original_image_url = ''
    zoom_raw = max(0.01, min(10.0, float(hero.get('zoom', 1.0))))
    return {
        'page_key': page_key,
        'label': paths['label'],
        'enabled': bool(hero.get('enabled', True) and image_exists),
        'image': hero.get('image', paths['final_rel']),
        'image_url': image_url,
        'position_x': max(pos_min, min(pos_max, int(hero.get('position_x', default_x)))),
        'position_y': max(pos_min, min(pos_max, int(hero.get('position_y', default_y)))),
        'zoom': zoom_raw,
        'crop_left': int(hero.get('crop_left', 0)),
        'crop_right': int(hero.get('crop_right', 0)),
        'crop_top': int(hero.get('crop_top', 0)),
        'crop_bottom': int(hero.get('crop_bottom', 0)),
        'overlay_opacity': float(hero.get('overlay_opacity', default_overlay)),
        'blur_enabled': bool(hero.get('blur_enabled', False)),
        'image_exists': image_exists,
        'original_image_exists': original_local_exists or original_storage_exists,
        'original_image_url': original_image_url,
    }


def update_page_hero_settings(page_key, form_data, image_file=None, delete_image=False):
    """Actualiza configuración de hero para una página y opcionalmente su imagen."""
    if page_key not in _PAGE_HERO_CONTEXTS:
        return False, "Contexto de portada no soportado."

    paths = _get_page_hero_paths(page_key)
    settings = _load_site_settings()
    settings.setdefault('page_heroes', {})
    hero_defaults = _default_site_settings()['page_heroes'][page_key]
    hero = settings['page_heroes'].get(page_key, hero_defaults.copy())
    settings['page_heroes'][page_key] = hero

    if delete_image:
        from app.database import get_supabase
        if not _serverless_read_only_fs_enabled():
            try:
                if paths['final_abs'].exists():
                    paths['final_abs'].unlink()
                if paths['original_abs'].exists():
                    paths['original_abs'].unlink()
            except OSError as e:
                if _is_read_only_fs_error(e):
                    logger.info("Limpieza local de hero omitida (filesystem solo lectura).")
                else:
                    logger.warning(f"No se pudieron eliminar respaldos locales del hero: {e}")
        if _hero_storage_enabled():
            try:
                get_supabase(role='service').storage.from_(_hero_storage_bucket()).remove([
                    paths['storage_final'],
                    paths['storage_original'],
                ])
                _HERO_STORAGE_FILES_CACHE['fetched_at'] = 0.0
            except Exception as e:
                logger.warning(f"No se pudo limpiar hero en Storage: {e}")
        settings['page_heroes'][page_key] = hero_defaults.copy()
        if not _save_site_settings(settings):
            return True, f"Portada de {paths['label']} restablecida, pero no se pudo persistir configuración avanzada."
        return True, f"Portada de {paths['label']} restablecida al estado por defecto."

    if image_file and image_file.filename:
        content = image_file.read()
        if not content:
            return False, "La imagen seleccionada está vacía."
        from flask import current_app
        max_size = current_app.config.get('MAX_HERO_UPLOAD_FILE_SIZE', 120 * 1024 * 1024)
        if len(content) > max_size:
            max_mb = round(max_size / (1024 * 1024), 1)
            return False, f"La imagen excede el tamaño máximo permitido ({max_mb} MB)."
        detected = imghdr.what(None, h=content)
        if detected not in {'png', 'jpeg', 'webp'}:
            return False, "Formato de imagen no válido para hero."
        try:
            optimized = _normalize_home_hero_image(content)
            if _hero_storage_enabled():
                if not _upload_storage_image_bytes(paths['storage_original'], optimized):
                    return False, "No se pudo guardar la imagen original en Storage."
                _HERO_STORAGE_FILES_CACHE['fetched_at'] = 0.0
            if not _serverless_read_only_fs_enabled():
                try:
                    paths['original_abs'].parent.mkdir(parents=True, exist_ok=True)
                    with paths['original_abs'].open('wb') as f:
                        f.write(optimized)
                except OSError as e:
                    if not _hero_storage_enabled():
                        raise
                    if _is_read_only_fs_error(e):
                        logger.info("Respaldo local de hero original omitido (filesystem solo lectura).")
                    else:
                        logger.warning(f"No se pudo guardar respaldo local de hero original: {e}")
            hero['image'] = paths['final_rel']
        except Exception as e:
            logger.error(f"No se pudo guardar imagen hero: {e}")
            return False, "No se pudo procesar la imagen del hero."

    def _safe_int(value, default):
        try:
            # Acepta valores decimales provenientes de sliders con step fino.
            return int(round(float(value)))
        except (TypeError, ValueError):
            return default

    def _safe_float(value, default):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    ui_hero = get_ui_settings().get('hero', {})
    pos_min = int(ui_hero.get('position_min', 0))
    pos_max = int(ui_hero.get('position_max', 200))
    default_x = int(ui_hero.get('default_position_x', 50))
    default_y = int(ui_hero.get('default_position_y', 45))
    zoom_min = float(ui_hero.get('zoom_min', 0.01))
    zoom_max = float(ui_hero.get('zoom_max', 10.0))
    default_zoom = float(ui_hero.get('default_zoom', 1.0))
    crop_min = int(ui_hero.get('crop_min', 0))
    crop_max = int(ui_hero.get('crop_max', 30))
    overlay_min = float(ui_hero.get('overlay_min', 0.0))
    overlay_max = float(ui_hero.get('overlay_max', 0.9))
    default_overlay = float(ui_hero.get('default_overlay_opacity', 0.45))

    hero['enabled'] = str(form_data.get('enabled', 'off')).lower() in {'1', 'true', 'on', 'yes'}
    hero['position_x'] = max(pos_min, min(pos_max, _safe_int(form_data.get('position_x', default_x), default_x)))
    hero['position_y'] = max(pos_min, min(pos_max, _safe_int(form_data.get('position_y', default_y), default_y)))
    hero['zoom'] = max(zoom_min, min(zoom_max, _safe_float(form_data.get('zoom', default_zoom), default_zoom)))
    hero['crop_left'] = max(crop_min, min(crop_max, _safe_int(form_data.get('crop_left', crop_min), crop_min)))
    hero['crop_right'] = max(crop_min, min(crop_max, _safe_int(form_data.get('crop_right', crop_min), crop_min)))
    hero['crop_top'] = max(crop_min, min(crop_max, _safe_int(form_data.get('crop_top', crop_min), crop_min)))
    hero['crop_bottom'] = max(crop_min, min(crop_max, _safe_int(form_data.get('crop_bottom', crop_min), crop_min)))
    hero['blur_enabled'] = str(form_data.get('blur_enabled', 'off')).lower() in {'1', 'true', 'on', 'yes'}

    if hero['crop_left'] + hero['crop_right'] >= 95:
        return False, "El recorte horizontal es excesivo. Ajusta izquierda/derecha."
    if hero['crop_top'] + hero['crop_bottom'] >= 95:
        return False, "El recorte vertical es excesivo. Ajusta superior/inferior."

    hero['overlay_opacity'] = max(overlay_min, min(overlay_max, _safe_float(form_data.get('overlay_opacity', default_overlay), default_overlay)))

    try:
        _build_page_hero_from_original(page_key, hero)
    except FileNotFoundError:
        return False, "Primero debes subir una imagen de portada."
    except Exception as e:
        logger.error(f"No se pudo regenerar hero final: {e}")
        return False, "No se pudo generar el encuadre final del hero."

    if not _save_site_settings(settings):
        return True, "Portada aplicada correctamente; no se pudo persistir el estado de controles (zoom/foco) en esta ejecución."
    return True, "Configuración de portada guardada."


def get_home_hero_settings():
    """Compatibilidad: retorna configuración del hero de home."""
    return get_page_hero_settings('home')


def update_home_hero_settings(form_data, image_file=None, delete_image=False):
    """Compatibilidad: actualiza configuración del hero de home."""
    return update_page_hero_settings('home', form_data, image_file=image_file, delete_image=delete_image)


# ═══════════════════════════════════════════════════════════════════════════════
#   NOTICIAS — Supabase table: public.news
# ═══════════════════════════════════════════════════════════════════════════════

def get_news(role='public'):
    """Retorna todas las noticias ordenadas por fecha descendente."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role=role).table('news').select('*').order('date', desc=True).execute()
        return resp.data or []
    except Exception as e:
        logger.error(f"Error al obtener noticias de Supabase: {e}")
        return []


def get_news_by_slug(slug, role='public'):
    """Retorna una noticia por su slug, o None."""
    from app.database import get_supabase
    try:
        candidates = [slug]
        decoded = unquote(slug or '')
        if decoded and decoded not in candidates:
            candidates.append(decoded)

        for candidate in candidates:
            resp = get_supabase(role=role).table('news').select('*').eq('slug', candidate).limit(1).execute()
            if resp.data:
                return resp.data[0]
        return None
    except Exception as e:
        logger.error(f"Error al obtener noticia '{slug}': {e}")
        return None


def get_news_by_id(news_id):
    """Retorna una noticia por id, o None (uso admin)."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('news').select('*').eq('id', news_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al obtener noticia id={news_id}: {e}")
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


def update_news_by_id(news_id, data):
    """Actualiza una noticia por id (uso admin)."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role='service').table('news').update(data).eq('id', news_id).execute()
        logger.info(f"Noticia actualizada en Supabase por id: {news_id}")
        return resp.data[0] if resp.data else None
    except Exception as e:
        logger.error(f"Error al actualizar noticia id={news_id}: {e}")
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


def delete_news_by_id(news_id):
    """Elimina una noticia por id (uso admin)."""
    from app.database import get_supabase
    try:
        get_supabase(role='service').table('news').delete().eq('id', news_id).execute()
        logger.info(f"Noticia eliminada de Supabase por id: {news_id}")
        return True
    except Exception as e:
        logger.error(f"Error al eliminar noticia id={news_id}: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   ACADÉMICOS — Supabase table: public.team_members
# ═══════════════════════════════════════════════════════════════════════════════

def get_team(role='public'):
    """Retorna todos los académicos."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role=role).table('team_members').select('*').order('name').execute()
        return resp.data or []
    except Exception as e:
        logger.error(f"Error al obtener equipo de Supabase: {e}")
        return []


def get_member_by_slug(slug, role='public'):
    """Retorna un académico por su slug, o None."""
    from app.database import get_supabase
    try:
        resp = get_supabase(role=role).table('team_members').select('*').eq('slug', slug).limit(1).execute()
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


def _normalize_avatar_image(content, size=300, quality=82):
    """Recorta al centro y redimensiona una imagen para avatar cuadrado."""
    with Image.open(BytesIO(content)) as img:
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        elif img.mode == 'RGBA':
            # Evita transparencia inesperada en salida comprimida.
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        width, height = img.size
        min_side = min(width, height)
        left = (width - min_side) // 2
        top = (height - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        img = img.crop((left, top, right, bottom))

        resampling = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS
        img = img.resize((size, size), resampling)

        out = BytesIO()
        img.save(out, format='WEBP', quality=quality, method=6)
        return out.getvalue()


def upload_to_storage(file, bucket='uploads', allowed_extensions=None, image_kind='default'):
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

    if image_kind == 'avatar':
        try:
            content = _normalize_avatar_image(content, size=300, quality=82)
            filename = secure_filename(f"{int(time.time())}_avatar.webp")
            content_type = 'image/webp'
        except Exception as e:
            logger.error(f"No se pudo normalizar avatar: {e}")
            return None

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
            name = f.get('name', '')
            if not name or name.startswith('.'):
                continue
            metadata = f.get('metadata') or {}
            size = metadata.get('size', 0)
            mimetype = str(metadata.get('mimetype', '')).lower()

            # Supabase puede devolver entradas de carpeta (ej: "hero") que no son archivos.
            # También ocultamos JSON interno de configuración del sistema.
            if '/' not in name and '.' not in name and (not mimetype or int(size or 0) == 0):
                continue
            if name.endswith('site-settings.json'):
                continue
            if mimetype and not mimetype.startswith('image/'):
                continue

            url = _get_storage_url(bucket, name)
            size_kb = round((float(size) if size else 0) / 1024, 1)
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


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
