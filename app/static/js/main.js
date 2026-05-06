/**
 * main.js — Lógica principal de la aplicación.
 * Responsabilidad: Inicializaciones generales, active nav highlighting.
 */

document.addEventListener('DOMContentLoaded', () => {
    if (window.appLog) window.appLog('INFO', 'DOMContentLoaded main.js');
    if (window.sendClientTrace) window.sendClientTrace('dom_ready', { label: 'main.js' });
    highlightActiveNav();
    initResponsiveHeroBackground();
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

/**
 * Ajusta el hero en móvil según la proporción real de la imagen de fondo.
 * No crea versiones extra: solo adapta encuadre/tamaño usando la misma imagen.
 */
function initResponsiveHeroBackground() {
    const heroes = document.querySelectorAll('.hero--with-image[data-hero-bg-url]');
    if (!heroes.length) return;
    const globalUIHero = (window.UI_SETTINGS && window.UI_SETTINGS.hero) || {};
    const globalUIPan = globalUIHero.mobile_pan || {};

    heroes.forEach(hero => {
        const bgUrl = hero.getAttribute('data-hero-bg-url');
        if (!bgUrl) return;

        const img = new Image();
        img.decoding = 'async';
        img.src = bgUrl;

        img.onload = () => {
            const width = Number(img.naturalWidth) || 0;
            const height = Number(img.naturalHeight) || 0;
            if (!width || !height) return;

            const ratio = width / height;
            hero.style.setProperty('--hero-image-ratio', ratio.toFixed(4));

            const getCssPercent = (name, fallback) => {
                const raw = getComputedStyle(hero).getPropertyValue(name).trim();
                const parsed = Number.parseFloat(raw);
                if (Number.isFinite(parsed)) return parsed;
                return fallback;
            };

            const getDataNumber = (name, fallback) => {
                const raw = hero.dataset[name];
                const parsed = Number.parseFloat(raw);
                if (Number.isFinite(parsed)) return parsed;
                return fallback;
            };

            const applyHeroMobilePan = () => {
                const viewportWidth = window.innerWidth || 0;
                const panBreakpoint = getDataNumber('heroPanBreakpoint', Number(globalUIPan.breakpoint ?? 768));
                if (viewportWidth > panBreakpoint) {
                    delete hero.dataset.heroPan;
                    hero.style.removeProperty('--hero-pan-start');
                    hero.style.removeProperty('--hero-pan-end');
                    hero.style.removeProperty('--hero-pan-duration');
                    hero.style.removeProperty('--hero-pan-y');
                    return;
                }

                hero.dataset.heroPan = 'active';
                const baseX = getCssPercent('--hero-bg-pos-x', 50);
                const baseY = getCssPercent('--hero-bg-pos-y', 45);
                hero.style.setProperty('--hero-pan-y', `${baseY}%`);
                const positionMin = getDataNumber('heroPositionMin', Number(globalUIHero.position_min ?? 0));
                const positionMax = getDataNumber('heroPositionMax', Number(globalUIHero.position_max ?? 200));

                const wideRatio = getDataNumber('heroPanWideRatio', Number(globalUIPan.wide_ratio ?? 1.6));
                const mediumRatio = getDataNumber('heroPanMediumRatio', Number(globalUIPan.medium_ratio ?? 1.2));
                const wideSweep = getDataNumber('heroPanWideSweep', Number(globalUIPan.wide_sweep ?? 44));
                const mediumSweep = getDataNumber('heroPanMediumSweep', Number(globalUIPan.medium_sweep ?? 30));
                const narrowSweep = getDataNumber('heroPanNarrowSweep', Number(globalUIPan.narrow_sweep ?? 18));
                const wideDuration = getDataNumber('heroPanWideDuration', Number(globalUIPan.duration_wide_s ?? 22));
                const mediumDuration = getDataNumber('heroPanMediumDuration', Number(globalUIPan.duration_medium_s ?? 24));
                const narrowDuration = getDataNumber('heroPanNarrowDuration', Number(globalUIPan.duration_narrow_s ?? 26));

                let sweep = narrowSweep;
                let duration = narrowDuration;

                if (ratio >= wideRatio) {
                    sweep = wideSweep;
                    duration = wideDuration;
                } else if (ratio >= mediumRatio) {
                    sweep = mediumSweep;
                    duration = mediumDuration;
                } else {
                    sweep = narrowSweep;
                    duration = narrowDuration;
                }

                const start = Math.max(positionMin, baseX - sweep);
                const end = Math.min(positionMax, baseX + sweep);
                hero.style.setProperty('--hero-pan-start', `${start}%`);
                hero.style.setProperty('--hero-pan-end', `${end}%`);
                hero.style.setProperty('--hero-pan-duration', `${duration}s`);
            };

            applyHeroMobilePan();
            window.addEventListener('resize', applyHeroMobilePan, { passive: true });

            if (window.appLog) {
                window.appLog('DEBUG', 'hero ratio detected', {
                    ratio: Number(ratio.toFixed(3)),
                    pan: hero.dataset.heroPan || 'desktop',
                    src: bgUrl,
                });
            }
        };
    });
}
