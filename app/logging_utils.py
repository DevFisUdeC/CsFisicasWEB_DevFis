"""
app/logging_utils.py — Utilidades de trazabilidad de funciones.
Responsabilidad: Decoradores para registrar entrada/salida/error de funciones.
"""

from __future__ import annotations

import functools
import logging
import time
from types import FunctionType
from typing import Any, Callable


def _short_repr(value: Any, max_len: int = 180) -> str:
    """Acorta repr para evitar logs gigantes o sensibles."""
    text = repr(value)
    if len(text) > max_len:
        return f"{text[:max_len]}...<trimmed>"
    return text


def trace_function(logger: logging.Logger | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorador de trazabilidad:
    - DEBUG: entrada con args/kwargs
    - DEBUG: salida con tiempo y tipo de retorno
    - ERROR: excepción con stack trace
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if getattr(func, "_is_traced", False):
            return func

        func_logger = logger or logging.getLogger(func.__module__)
        qualname = func.__qualname__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            started = time.perf_counter()
            func_logger.debug(
                "ENTER %s | args=%s | kwargs=%s",
                qualname,
                _short_repr(args),
                _short_repr(kwargs),
            )
            try:
                result = func(*args, **kwargs)
                elapsed_ms = (time.perf_counter() - started) * 1000
                func_logger.debug(
                    "EXIT %s | elapsed_ms=%.2f | result_type=%s | result=%s",
                    qualname,
                    elapsed_ms,
                    type(result).__name__,
                    _short_repr(result),
                )
                return result
            except Exception:
                elapsed_ms = (time.perf_counter() - started) * 1000
                func_logger.exception(
                    "ERROR %s | elapsed_ms=%.2f",
                    qualname,
                    elapsed_ms,
                )
                raise

        wrapper._is_traced = True  # type: ignore[attr-defined]
        return wrapper

    return decorator


def auto_trace_module_functions(
    module_globals: dict[str, Any],
    logger: logging.Logger | None = None,
    exclude: set[str] | None = None,
) -> None:
    """Instrumenta automáticamente todas las funciones definidas en el módulo."""
    exclude = exclude or set()
    module_name = module_globals.get("__name__", "")
    tracer = trace_function(logger)

    for name, obj in list(module_globals.items()):
        if name.startswith("_") and name not in {"_is_safe_next_url", "_upload"}:
            continue
        if name in exclude:
            continue
        if not isinstance(obj, FunctionType):
            continue
        if obj.__module__ != module_name:
            continue
        module_globals[name] = tracer(obj)
