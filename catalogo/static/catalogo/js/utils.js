// ==================== UTILIDADES GENERALES ====================

function mostrarNotificacion(mensaje, tipo = 'info', duracion = 3000) {
    let contenedor = document.getElementById('toast-container');
    if (!contenedor) {
        contenedor = document.createElement('div');
        contenedor.id = 'toast-container';
        contenedor.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
        document.body.appendChild(contenedor);
    }

    const clases = { success: 'alert alert-success', error: 'alert alert-danger', warning: 'alert alert-warning', info: 'alert alert-info' };
    const toast = document.createElement('div');
    toast.className = clases[tipo] || clases.info;
    toast.style.animation = 'slideIn 0.3s ease-in';
    toast.textContent = mensaje;
    contenedor.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, duracion);
}

function confirmar(mensaje) {
    return confirm(mensaje);
}

function validarEmail(email) {
    return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

function validarContrasena(password) {
    const resultado = { valido: true, errores: [] };
    if (password.length < 8)     { resultado.valido = false; resultado.errores.push('La contraseña debe tener al menos 8 caracteres'); }
    if (!/[A-Z]/.test(password)) { resultado.valido = false; resultado.errores.push('Debe contener al menos una mayúscula'); }
    if (!/[0-9]/.test(password)) { resultado.valido = false; resultado.errores.push('Debe contener al menos un número'); }
    return resultado;
}

function formatoMoneda(numero) {
    return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(numero);
}

function formatoFecha(fecha) {
    return new Intl.DateTimeFormat('es-MX', {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    }).format(new Date(fecha));
}

function cargarContenido(url, selector) {
    fetch(url)
        .then(r => r.text())
        .then(data => { document.querySelector(selector).innerHTML = data; })
        .catch(() => mostrarNotificacion('Error al cargar contenido', 'error'));
}

function enviarFormularioAjax(formulario, url, callback) {
    fetch(url, {
        method: 'POST',
        body: new FormData(formulario),
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(r => r.json())
    .then(data => {
        mostrarNotificacion(data.mensaje || (data.success ? 'Operación completada' : 'Error en la operación'), data.success ? 'success' : 'error');
        if (data.success && callback) callback(data);
    })
    .catch(() => mostrarNotificacion('Error en la operación', 'error'));
}

function initTablaBusqueda(idTabla, idBusqueda) {
    const tabla = document.getElementById(idTabla);
    const input = document.getElementById(idBusqueda);
    if (!tabla || !input) return;
    input.addEventListener('keyup', function () {
        const t = this.value.toLowerCase();
        tabla.querySelectorAll('tbody tr').forEach(fila => {
            fila.style.display = fila.textContent.toLowerCase().includes(t) ? '' : 'none';
        });
    });
}

function inicializarTooltips() {
    [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        .forEach(el => new bootstrap.Tooltip(el));
}

function inicializarPopovers() {
    [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
        .forEach(el => new bootstrap.Popover(el));
}

// Inyectar animaciones usadas por las notificaciones toast
(function () {
    const s = document.createElement('style');
    s.textContent = `
        @keyframes slideIn  { from { transform:translateX(100%); opacity:0; } to { transform:translateX(0); opacity:1; } }
        @keyframes slideOut { from { transform:translateX(0); opacity:1; } to { transform:translateX(100%); opacity:0; } }
        @keyframes fadeIn   { from { opacity:0; } to { opacity:1; } }
    `;
    document.head.appendChild(s);
})();
