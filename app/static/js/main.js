/**
 * main.js — Lógica principal de la aplicación.
 * Responsabilidad: Inicializaciones generales, active nav highlighting.
 */

document.addEventListener('DOMContentLoaded', () => {
    highlightActiveNav();
});


/**
 * Marca como activo el enlace de navegación que corresponde a la URL actual.
 */
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar__link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('navbar__link--active');
        }
    });
}
