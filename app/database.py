"""
app/database.py — Cliente Supabase centralizado.
Responsabilidad: Inicializar y proveer el cliente Supabase (service_role)
para operaciones CRUD desde el backend Flask.
"""

import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

_supabase: Client | None = None


def init_supabase(app) -> Client:
    """Inicializa el cliente Supabase con la service_key del config de Flask."""
    global _supabase
    url = app.config.get('SUPABASE_URL', '')
    key = app.config.get('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        logger.error("SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas.")
        raise RuntimeError("Faltan credenciales de Supabase. Revisa tu .env")
    _supabase = create_client(url, key)
    logger.info("Cliente Supabase inicializado correctamente.")
    return _supabase


def get_supabase() -> Client:
    """Retorna el cliente Supabase ya inicializado."""
    if _supabase is None:
        raise RuntimeError("Supabase no inicializado. Llama init_supabase(app) primero.")
    return _supabase
