/**
 * navigation.js — Lógica del menú de navegación responsive.
 * Responsabilidad: Toggle del menú móvil y cierre al hacer click fuera.
 */

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    if (window.appLog) window.appLog('INFO', 'DOMContentLoaded navigation.js');
    if (window.sendClientTrace) window.sendClientTrace('dom_ready', { label: 'navigation.js' });
    if (window.appLog) window.appLog('DEBUG', 'navigation elements resolved', { hasToggle: !!toggle, hasMobileMenu: !!mobileMenu });

    if (!toggle || !mobileMenu) {
        if (window.appLog) window.appLog('WARNING', 'mobile menu elements not found');
        if (window.sendClientTrace) window.sendClientTrace('menu_missing', { label: 'mobile_menu_elements' });
        return;
    }

    toggle.addEventListener('click', () => {
        const isOpen = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !isOpen);
        mobileMenu.hidden = isOpen;

        // Animate hamburger
        toggle.classList.toggle('is-active', !isOpen);
        if (window.appLog) window.appLog('INFO', 'mobile menu toggled', { open: !isOpen });
        if (window.sendClientTrace) window.sendClientTrace('menu_toggle', { label: !isOpen ? 'open' : 'close' });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !mobileMenu.contains(e.target)) {
            toggle.setAttribute('aria-expanded', 'false');
            mobileMenu.hidden = true;
            toggle.classList.remove('is-active');
            if (window.appLog) window.appLog('DEBUG', 'mobile menu closed by outside click');
            if (window.sendClientTrace) window.sendClientTrace('menu_close_outside', { label: 'outside_click' });
        }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggle.setAttribute('aria-expanded', 'false');
            mobileMenu.hidden = true;
            toggle.classList.remove('is-active');
            if (window.appLog) window.appLog('DEBUG', 'mobile menu closed by escape');
            if (window.sendClientTrace) window.sendClientTrace('menu_close_escape', { label: 'escape' });
        }
    });
});
