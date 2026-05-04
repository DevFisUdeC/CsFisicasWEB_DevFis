/**
 * main.js — Lógica principal de la aplicación.
 * Responsabilidad: Inicializaciones generales, active nav highlighting.
 */

document.addEventListener('DOMContentLoaded', () => {
    if (window.appLog) window.appLog('INFO', 'DOMContentLoaded main.js');
    if (window.sendClientTrace) window.sendClientTrace('dom_ready', { label: 'main.js' });
    highlightActiveNav();
    traceInteractiveElements();
});


/**
 * Marca como activo el enlace de navegación que corresponde a la URL actual.
 */
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar__link');
    if (window.appLog) window.appLog('DEBUG', 'highlightActiveNav start', { currentPath, navLinkCount: navLinks.length });

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('navbar__link--active');
            if (window.appLog) window.appLog('DEBUG', 'navbar active link', { href, currentPath });
        }
    });
    if (window.appLog) window.appLog('DEBUG', 'highlightActiveNav end');
    if (window.sendClientTrace) window.sendClientTrace('nav_highlight_complete', { label: currentPath });
}

function traceInteractiveElements() {
    const trackedSelectors = [
        '.navbar__link',
        '.navbar__dropdown-link',
        '.navbar__mobile-link',
        '.navbar__mobile-sublink',
        '.btn',
        'a',
    ];

    trackedSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.addEventListener('click', () => {
                if (!window.appLog) return;
                const payload = {
                    selector,
                    text: (el.textContent || '').trim().slice(0, 80),
                    href: el.getAttribute('href') || null,
                };
                window.appLog('INFO', 'click detected', {
                    selector: payload.selector,
                    text: payload.text,
                    href: payload.href,
                });
                if (window.sendClientTrace) {
                    window.sendClientTrace('click', {
                        label: payload.text || selector,
                        href: payload.href,
                        meta: { selector: payload.selector },
                    });
                }
            });
        });
    });

    if (window.appLog) {
        window.appLog('DEBUG', 'interactive tracing ready', { selectors: trackedSelectors });
    }

    document.querySelectorAll('iframe').forEach((frame, idx) => {
        frame.addEventListener('load', () => {
            if (window.appLog) {
                window.appLog('INFO', 'iframe loaded', { index: idx, src: frame.src || null });
            }
            if (window.sendClientTrace) {
                window.sendClientTrace('iframe_loaded', {
                    label: `iframe_${idx}`,
                    href: frame.src || null,
                });
            }
        });
    });

    document.querySelectorAll('img').forEach((img, idx) => {
        img.addEventListener('error', () => {
            if (window.appLog) {
                window.appLog('ERROR', 'image load failed', { index: idx, src: img.src || null });
            }
            if (window.sendClientTrace) {
                window.sendClientTrace('image_error', {
                    label: `img_${idx}`,
                    href: img.src || null,
                });
            }
        });
    });
}
