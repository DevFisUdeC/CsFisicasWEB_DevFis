/**
 * navigation.js — Lógica del menú de navegación responsive.
 * Responsabilidad: Toggle del menú móvil y cierre al hacer click fuera.
 */

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    if (!toggle || !mobileMenu) return;

    toggle.addEventListener('click', () => {
        const isOpen = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !isOpen);
        mobileMenu.hidden = isOpen;

        // Animate hamburger
        toggle.classList.toggle('is-active', !isOpen);
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !mobileMenu.contains(e.target)) {
            toggle.setAttribute('aria-expanded', 'false');
            mobileMenu.hidden = true;
            toggle.classList.remove('is-active');
        }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggle.setAttribute('aria-expanded', 'false');
            mobileMenu.hidden = true;
            toggle.classList.remove('is-active');
        }
    });
});
