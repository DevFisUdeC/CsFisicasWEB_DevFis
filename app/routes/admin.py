"""
app/routes/admin.py — Panel de Control CMS Custom.
Responsabilidad: Rutas CRUD del panel de administración (noticias, académicos, imágenes).
Datos: Supabase (PostgreSQL + Storage).
"""

from datetime import datetime
from urllib.parse import urlparse
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import logging
from app.helpers import (
    get_news, get_news_by_slug, create_news, update_news, delete_news_by_slug,
    get_team, get_member_by_slug, create_team_member, update_team_member, delete_team_member_by_slug,
    upload_to_storage, list_storage_files, delete_from_storage,
    slugify,
)
from app.auth import login_required
from app.logging_utils import auto_trace_module_functions

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


def _is_safe_next_url(next_url: str | None) -> bool:
    """Permite solo redirecciones internas relativas al sitio."""
    if not next_url:
        logger.debug("safe_next_url | vacío o nulo")
        return False
    parsed = urlparse(next_url)
    logger.debug("safe_next_url | next=%s | scheme=%s | netloc=%s", next_url, parsed.scheme, parsed.netloc)
    return parsed.scheme == '' and parsed.netloc == '' and next_url.startswith('/') and not next_url.startswith('//')


# ─── Context Processor: inyecta contadores en todas las vistas admin ────────

@admin_bp.context_processor
def inject_admin_counts():
    """Contadores disponibles en todos los templates admin (sidebar badges)."""
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    return {
        'news_count': len(get_news()),
        'team_count': len(get_team()),
        'images_count': len(list_storage_files(bucket)),
    }


# ─── Helper interno ─────────────────────────────────────────────────────────

def _upload(file_field):
    """Atajo para subir un archivo a Supabase Storage desde request.files."""
    logger.debug("upload helper | file_field=%s", file_field)
    f = request.files.get(file_field)
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp'})
    return upload_to_storage(f, bucket=bucket, allowed_extensions=allowed)


# ═══════════════════════════════════════════════════════════════════════════════
#   AUTH
# ═══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Autenticación para la periodista."""
    from werkzeug.security import check_password_hash

    error = None
    if request.method == 'POST':
        username_ok = request.form['username'] == current_app.config['ADMIN_USER']

        pass_hash = current_app.config.get('ADMIN_PASS_HASH', '')
        if pass_hash:
            password_ok = check_password_hash(pass_hash, request.form['password'])
        else:
            password_ok = request.form['password'] == current_app.config['ADMIN_PASS']

        if not (username_ok and password_ok):
            error = 'Credenciales inválidas. Por favor intente nuevamente.'
            current_app.logger.warning(
                f"Intento de login fallido en panel admin. Usuario provisto: {request.form['username']}")
        else:
            session['logged_in'] = True
            session.permanent = True
            current_app.logger.info("Admin login exitoso")
            flash("Bienvenido al Panel de Administración", "success")
            next_url = request.args.get('next')
            if _is_safe_next_url(next_url):
                return redirect(next_url)
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html', error=error)


@admin_bp.route('/logout')
def logout():
    """Cierra sesión."""
    session.pop('logged_in', None)
    flash("Sesión cerrada exitosamente.", "info")
    current_app.logger.info("Sesión de admin cerrada.")
    return redirect(url_for('main.home'))


# ═══════════════════════════════════════════════════════════════════════════════
#   DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/')
@login_required
def dashboard():
    """Dashboard con resumen general."""
    news = get_news()
    team = get_team()
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    images = list_storage_files(bucket)
    return render_template('admin/dashboard.html',
                           news=news, team=team, images=images,
                           active_section='dashboard')


# ═══════════════════════════════════════════════════════════════════════════════
#   NOTICIAS CRUD
# ═══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/news')
@login_required
def news_list():
    """Listado de noticias."""
    news = get_news()
    return render_template('admin/news.html', news=news, active_section='news')


@admin_bp.route('/news/create', methods=['GET', 'POST'])
@login_required
def create_news_view():
    """Formulario para crear una noticia nueva."""
    if request.method == 'POST':
        image_url = _upload('image')
        data = {
            "slug": slugify(request.form['title']),
            "title": request.form['title'],
            "date": request.form['date'],
            "category": request.form['category'],
            "summary": request.form['summary'],
            "content": request.form['content'],
            "image": image_url,
            "source": request.form.get('source') or None,
        }
        result = create_news(data)
        if result:
            flash("¡Noticia publicada exitosamente!", "success")
        else:
            flash("Error al crear la noticia. Intente nuevamente.", "error")
        return redirect(url_for('admin.news_list'))

    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('admin/news_form.html',
                           article=None, today_date=today,
                           active_section='news')


@admin_bp.route('/news/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit_news_view(slug):
    """Editor individual para una noticia."""
    article = get_news_by_slug(slug)
    if not article:
        flash("Noticia no encontrada.", "error")
        return redirect(url_for('admin.news_list'))

    if request.method == 'POST':
        data = {
            "title": request.form['title'],
            "date": request.form['date'],
            "category": request.form['category'],
            "summary": request.form['summary'],
            "content": request.form['content'],
            "source": request.form.get('source') or None,
        }
        new_image = _upload('image')
        if new_image:
            data['image'] = new_image
        result = update_news(slug, data)
        if result:
            flash("La noticia ha sido actualizada.", "success")
        else:
            flash("Error al actualizar la noticia.", "error")
        return redirect(url_for('admin.news_list'))

    return render_template('admin/news_form.html',
                           article=article, active_section='news')


@admin_bp.route('/news/delete/<slug>', methods=['POST'])
@login_required
def delete_news_view(slug):
    """Elimina una noticia específica."""
    if delete_news_by_slug(slug):
        flash("Noticia eliminada permanentemente.", "warning")
    else:
        flash("Error al eliminar la noticia.", "error")
    return redirect(url_for('admin.news_list'))


# ═══════════════════════════════════════════════════════════════════════════════
#   ACADÉMICOS CRUD
# ═══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/team')
@login_required
def team_list():
    """Listado de académicos."""
    team = get_team()
    return render_template('admin/team.html', team=team, active_section='team')


@admin_bp.route('/team/create', methods=['GET', 'POST'])
@login_required
def create_member():
    """Formulario para agregar un nuevo académico."""
    if request.method == 'POST':
        photo_url = _upload('photo')
        lines_raw = request.form.get('research_lines', '')
        research_lines = [l.strip() for l in lines_raw.split(',') if l.strip()]
        data = {
            "slug": slugify(request.form['name']),
            "name": request.form['name'],
            "title": request.form['title'],
            "role": request.form['role'],
            "area": request.form['area'],
            "email": request.form['email'],
            "office": request.form.get('office', ''),
            "bio": request.form.get('bio', ''),
            "research_lines": research_lines,
            "photo": photo_url,
        }
        result = create_team_member(data)
        if result:
            flash(f"Académico '{request.form['name']}' agregado exitosamente.", "success")
        else:
            flash("Error al crear el académico.", "error")
        return redirect(url_for('admin.team_list'))

    return render_template('admin/team_form.html',
                           member=None, active_section='team')


@admin_bp.route('/team/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit_member(slug):
    """Editor individual para un académico."""
    member = get_member_by_slug(slug)
    if not member:
        flash("Académico no encontrado.", "error")
        return redirect(url_for('admin.team_list'))

    if request.method == 'POST':
        lines_raw = request.form.get('research_lines', '')
        data = {
            "name": request.form['name'],
            "title": request.form['title'],
            "role": request.form['role'],
            "area": request.form['area'],
            "email": request.form['email'],
            "office": request.form.get('office', ''),
            "bio": request.form.get('bio', ''),
            "research_lines": [l.strip() for l in lines_raw.split(',') if l.strip()],
        }
        new_photo = _upload('photo')
        if new_photo:
            data['photo'] = new_photo
        result = update_team_member(slug, data)
        if result:
            flash(f"Académico '{request.form['name']}' actualizado.", "success")
        else:
            flash("Error al actualizar el académico.", "error")
        return redirect(url_for('admin.team_list'))

    return render_template('admin/team_form.html',
                           member=member, active_section='team')


@admin_bp.route('/team/delete/<slug>', methods=['POST'])
@login_required
def delete_member(slug):
    """Elimina un académico."""
    if delete_team_member_by_slug(slug):
        flash("Académico eliminado permanentemente.", "warning")
    else:
        flash("Error al eliminar el académico.", "error")
    return redirect(url_for('admin.team_list'))


# ═══════════════════════════════════════════════════════════════════════════════
#   GALERÍA DE IMÁGENES
# ═══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/images')
@login_required
def image_gallery():
    """Galería de imágenes subidas a Supabase Storage."""
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    images = list_storage_files(bucket)
    return render_template('admin/images.html',
                           images=images, active_section='images')


@admin_bp.route('/images/upload', methods=['POST'])
@login_required
def upload_image():
    """Sube una o más imágenes a Supabase Storage."""
    files = request.files.getlist('images')
    max_files = current_app.config.get('MAX_UPLOAD_FILES', 10)
    if len(files) > max_files:
        flash(f"Máximo permitido por carga: {max_files} archivos.", "error")
        return redirect(url_for('admin.image_gallery'))
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp'})
    uploaded = 0
    for f in files:
        result = upload_to_storage(f, bucket=bucket, allowed_extensions=allowed)
        if result:
            uploaded += 1
    if uploaded:
        current_app.logger.info(f"{uploaded} imagen(es) subida(s) a Supabase Storage.")
        flash(f"{uploaded} imagen(es) subida(s) exitosamente.", "success")
    else:
        flash("No se pudo subir ninguna imagen. Revise el formato.", "error")
    return redirect(url_for('admin.image_gallery'))


@admin_bp.route('/images/delete', methods=['POST'])
@login_required
def delete_image():
    """Elimina una imagen de Supabase Storage."""
    filename = request.form.get('filename', '')
    bucket = current_app.config.get('SUPABASE_BUCKET', 'uploads')
    if delete_from_storage(filename, bucket=bucket):
        flash("Imagen eliminada.", "warning")
    else:
        flash("No se pudo eliminar la imagen.", "error")
    return redirect(url_for('admin.image_gallery'))


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
