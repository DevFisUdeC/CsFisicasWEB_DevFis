/**
 * debug-trace.js — Trazabilidad total para desarrollo.
 * Se carga solo en DEBUG desde base.html.
 */

(function () {
    if (!window.APP_DEBUG || !window.sendClientTrace) return;

    function safeText(value, maxLen) {
        const text = String(value || '');
        return text.length > maxLen ? text.slice(0, maxLen) : text;
    }

    function trace(eventName, payload) {
        window.sendClientTrace(eventName, payload || {});
    }

    function getTargetDescriptor(el) {
        if (!el) return 'unknown';
        const id = el.id ? `#${el.id}` : '';
        const cls = el.className && typeof el.className === 'string'
            ? '.' + el.className.trim().replace(/\s+/g, '.')
            : '';
        return `${(el.tagName || 'node').toLowerCase()}${id}${cls}`.slice(0, 180);
    }

    trace('debug_trace_boot', { label: 'debug-trace.js loaded', level: 'info' });

    // Clicks globales (captura)
    document.addEventListener('click', (e) => {
        const t = e.target;
        const clickable = t && t.closest ? t.closest('a,button,input[type="button"],input[type="submit"],summary,[role="button"]') : null;
        const target = clickable || t;

        const href = clickable && clickable.getAttribute ? clickable.getAttribute('href') : '';
        const label = safeText(target && target.textContent ? target.textContent.trim() : target && target.value ? target.value : '', 120);

        trace('ui_click', {
            label: label || getTargetDescriptor(target),
            href: href || '',
            level: 'info',
            meta: {
                descriptor: getTargetDescriptor(target),
            },
        });
    }, true);

    // Cambios en formularios
    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (!form) return;
        const action = form.getAttribute('action') || window.location.pathname;
        trace('form_submit', {
            label: safeText(form.getAttribute('id') || form.getAttribute('name') || 'form_submit', 120),
            href: action,
            level: 'info',
            meta: {
                method: (form.getAttribute('method') || 'get').toUpperCase(),
                fields: Array.from(form.elements || [])
                    .map((el) => (el && (el.name || el.id)) ? (el.name || el.id) : null)
                    .filter(Boolean)
                    .slice(0, 30),
            },
        });
    }, true);

    document.addEventListener('change', (e) => {
        const t = e.target;
        if (!t) return;
        const name = t.name || t.id || getTargetDescriptor(t);
        trace('field_change', {
            label: safeText(name, 120),
            level: 'debug',
            meta: {
                type: t.type || t.tagName,
                value_length: (t.value || '').length,
            },
        });
    }, true);

    // Navegación / ciclo de página
    window.addEventListener('beforeunload', () => {
        trace('before_unload', { label: window.location.pathname, level: 'debug' });
    });

    window.addEventListener('pagehide', () => {
        trace('page_hide', { label: window.location.pathname, level: 'debug' });
    });

    window.addEventListener('pageshow', () => {
        trace('page_show', { label: window.location.pathname, level: 'debug' });
    });

    window.addEventListener('hashchange', () => {
        trace('hash_change', { label: window.location.hash || '#', level: 'debug' });
    });

    window.addEventListener('popstate', () => {
        trace('popstate', { label: window.location.pathname, level: 'debug' });
    });

    document.addEventListener('visibilitychange', () => {
        trace('visibility_change', {
            label: document.visibilityState,
            level: 'debug',
        });
    });

    // Errores frontend
    window.addEventListener('error', (e) => {
        trace('js_error', {
            label: safeText(e.message || 'window.error', 120),
            level: 'error',
            meta: {
                file: e.filename || '',
                line: e.lineno || 0,
                col: e.colno || 0,
            },
        });
    });

    window.addEventListener('unhandledrejection', (e) => {
        const reason = e.reason && e.reason.message ? e.reason.message : String(e.reason || 'promise rejection');
        trace('promise_rejection', {
            label: safeText(reason, 120),
            level: 'error',
        });
    });

    // Trazas de red frontend (fetch + XHR)
    const originalFetch = window.fetch;
    window.fetch = function (...args) {
        const started = performance.now();
        let url = '';
        let method = 'GET';
        try {
            const input = args[0];
            const init = args[1] || {};
            url = typeof input === 'string' ? input : (input && input.url) ? input.url : '';
            method = (init.method || (input && input.method) || 'GET').toUpperCase();
        } catch (_) {}

        return originalFetch.apply(this, args)
            .then((resp) => {
                trace('fetch_response', {
                    label: `${method} ${safeText(url, 140)}`,
                    level: resp.ok ? 'debug' : 'warning',
                    meta: {
                        status: resp.status,
                        elapsed_ms: Number((performance.now() - started).toFixed(2)),
                    },
                });
                return resp;
            })
            .catch((err) => {
                trace('fetch_error', {
                    label: `${method} ${safeText(url, 140)}`,
                    level: 'error',
                    meta: {
                        error: safeText(err && err.message ? err.message : String(err), 160),
                        elapsed_ms: Number((performance.now() - started).toFixed(2)),
                    },
                });
                throw err;
            });
    };

    const originalOpen = XMLHttpRequest.prototype.open;
    const originalSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function (method, url, ...rest) {
        this.__traceMethod = method;
        this.__traceUrl = url;
        this.__traceStart = performance.now();
        return originalOpen.call(this, method, url, ...rest);
    };

    XMLHttpRequest.prototype.send = function (...args) {
        this.addEventListener('loadend', () => {
            trace('xhr_response', {
                label: `${(this.__traceMethod || 'GET').toUpperCase()} ${safeText(this.__traceUrl || '', 140)}`,
                level: this.status >= 200 && this.status < 400 ? 'debug' : 'warning',
                meta: {
                    status: this.status,
                    elapsed_ms: Number((performance.now() - (this.__traceStart || performance.now())).toFixed(2)),
                },
            });
        });
        return originalSend.apply(this, args);
    };
})();
