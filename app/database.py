"""
app/database.py — Cliente Supabase centralizado.
Responsabilidad: Inicializar y proveer el cliente Supabase (service_role)
para operaciones CRUD desde el backend Flask.
"""

import logging
from supabase import create_client, Client
from app.logging_utils import auto_trace_module_functions

logger = logging.getLogger(__name__)

_supabase_service: Client | None = None
_supabase_public: Client | None = None


def init_supabase(app) -> Client:
    """Inicializa clientes Supabase (service + public)."""
    global _supabase_service, _supabase_public
    url = app.config.get('SUPABASE_URL', '')
    service_key = app.config.get('SUPABASE_SERVICE_KEY', '')
    anon_key = app.config.get('SUPABASE_ANON_KEY', '')
    if not url or not service_key:
        logger.error("SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas.")
        raise RuntimeError("Faltan credenciales de Supabase. Revisa tu .env")
    _supabase_service = create_client(url, service_key)
    if anon_key:
        _supabase_public = create_client(url, anon_key)
        logger.info("Clientes Supabase inicializados: service y public.")
    else:
        _supabase_public = _supabase_service
        logger.warning("SUPABASE_ANON_KEY no configurada; cliente public usa service_role (menos seguro).")
    return _supabase_service


def get_supabase(role: str = 'service') -> Client:
    """Retorna cliente Supabase según rol: service/public."""
    if role == 'public':
        if _supabase_public is None:
            raise RuntimeError("Supabase public no inicializado. Llama init_supabase(app) primero.")
        return _supabase_public
    if _supabase_service is None:
        raise RuntimeError("Supabase no inicializado. Llama init_supabase(app) primero.")
    return _supabase_service


auto_trace_module_functions(
    globals(),
    logger=logger,
    exclude={'auto_trace_module_functions'}
)
