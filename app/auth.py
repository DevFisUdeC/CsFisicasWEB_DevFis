"""
app/auth.py — Autenticación y control de acceso.
Responsabilidad: Decoradores y lógica de autenticación para el panel admin.
"""

from functools import wraps
from flask import session, redirect, url_for, request
import logging

from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)


def login_required(f):
    """Decorador que restringe acceso a usuarios autenticados."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug("AUTH CHECK | path=%s | logged_in=%s", request.path, bool(session.get('logged_in')))
        if not session.get('logged_in'):
            # Usar request.path en lugar de request.url para evitar URLs absolutas
            logger.warning("AUTH BLOCKED | redirect_login | path=%s", request.path)
            return redirect(url_for('admin.login', next=request.path))
        logger.debug("AUTH OK | path=%s", request.path)
        return f(*args, **kwargs)
    return decorated_function


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
