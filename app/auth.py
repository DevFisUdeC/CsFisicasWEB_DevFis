"""
app/auth.py — Autenticación y control de acceso.
Responsabilidad: Decoradores y lógica de autenticación para el panel admin.
"""

from functools import wraps
from flask import session, redirect, url_for, request


def login_required(f):
    """Decorador que restringe acceso a usuarios autenticados."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            # Usar request.path en lugar de request.url para evitar URLs absolutas
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
