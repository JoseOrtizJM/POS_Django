// ==================== INICIALIZACIÓN ====================
// Punto de entrada: inicializa Bootstrap tooltips/popovers y widgets del carrito.
// Usa typeof para no romper si carrito.js fue bloqueado por el navegador.

document.addEventListener('DOMContentLoaded', function () {
    if (typeof inicializarTooltips  === 'function') inicializarTooltips();
    if (typeof inicializarPopovers  === 'function') inicializarPopovers();
    if (typeof initCarritoWidgets   === 'function') initCarritoWidgets();
});
