// ==================== UTILIDADES GENERALES ====================

/**
 * Muestra una notificación toast
 * @param {string} mensaje - El mensaje a mostrar
 * @param {string} tipo - El tipo de notificación (success, error, warning, info)
 * @param {number} duracion - Duración en milisegundos
 */
function mostrarNotificacion(mensaje, tipo = 'info', duracion = 3000) {
    // Crear contenedor si no existe
    let contenedor = document.getElementById('toast-container');
    if (!contenedor) {
        contenedor = document.createElement('div');
        contenedor.id = 'toast-container';
        contenedor.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(contenedor);
    }

    // Crear elemento toast
    const toast = document.createElement('div');
    const clases = {
        success: 'alert alert-success',
        error: 'alert alert-danger',
        warning: 'alert alert-warning',
        info: 'alert alert-info'
    };
    
    toast.className = clases[tipo] || clases.info;
    toast.style.cssText = 'animation: slideIn 0.3s ease-in;';
    toast.textContent = mensaje;
    
    contenedor.appendChild(toast);

    // Eliminar después de duracion
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, duracion);
}

/**
 * Confirma una acción antes de ejecutarla
 * @param {string} mensaje - Mensaje de confirmación
 * @returns {boolean} true si el usuario confirma, false si cancela
 */
function confirmar(mensaje) {
    return confirm(mensaje);
}

/**
 * Valida que un email tenga formato correcto
 * @param {string} email - Email a validar
 * @returns {boolean} true si es válido, false si no
 */
function validarEmail(email) {
    const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return patron.test(email);
}

/**
 * Valida que una contraseña cumpla requisitos mínimos
 * @param {string} password - Contraseña a validar
 * @returns {object} Objeto con la validación y mensajes
 */
function validarContrasena(password) {
    const resultado = {
        valido: true,
        errores: []
    };

    if (password.length < 8) {
        resultado.valido = false;
        resultado.errores.push('La contraseña debe tener al menos 8 caracteres');
    }

    if (!/[A-Z]/.test(password)) {
        resultado.valido = false;
        resultado.errores.push('Debe contener al menos una mayúscula');
    }

    if (!/[0-9]/.test(password)) {
        resultado.valido = false;
        resultado.errores.push('Debe contener al menos un número');
    }

    return resultado;
}

/**
 * Formatea un número como moneda mexicana
 * @param {number} numero - Número a formatear
 * @returns {string} Número formateado como moneda
 */
function formatoMoneda(numero) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(numero);
}

/**
 * Formatea una fecha en formato legible
 * @param {string} fecha - Fecha en formato ISO
 * @returns {string} Fecha formateada
 */
function formatoFecha(fecha) {
    return new Intl.DateTimeFormat('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(fecha));
}

/**
 * Carga contenido dinámicamente
 * @param {string} url - URL a cargar
 * @param {string} selector - Selector CSS donde insertar el contenido
 */
function cargarContenido(url, selector) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.querySelector(selector).innerHTML = data;
        })
        .catch(error => {
            console.error('Error al cargar contenido:', error);
            mostrarNotificacion('Error al cargar contenido', 'error');
        });
}

/**
 * Envía un formulario por AJAX
 * @param {HTMLFormElement} formulario - El formulario a enviar
 * @param {string} url - URL de destino
 * @param {function} callback - Función a ejecutar después de enviar
 */
function enviarFormularioAjax(formulario, url, callback) {
    const formData = new FormData(formulario);
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarNotificacion(data.mensaje || 'Operación completada', 'success');
            if (callback) callback(data);
        } else {
            mostrarNotificacion(data.mensaje || 'Error en la operación', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error en la operación', 'error');
    });
}

/**
 * Tabla con funcionalidad de búsqueda y filtrado
 * @param {string} idTabla - ID de la tabla
 * @param {string} idBusqueda - ID del input de búsqueda
 */
function initTablaBusqueda(idTabla, idBusqueda) {
    const tabla = document.getElementById(idTabla);
    const inputBusqueda = document.getElementById(idBusqueda);

    if (!tabla || !inputBusqueda) return;

    inputBusqueda.addEventListener('keyup', function() {
        const termino = this.value.toLowerCase();
        const filas = tabla.querySelectorAll('tbody tr');

        filas.forEach(fila => {
            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(termino) ? '' : 'none';
        });
    });
}

/**
 * Inicializa tooltips de Bootstrap
 */
function inicializarTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializa popovers de Bootstrap
 */
function inicializarPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ==================== ANIMACIONES ====================

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Inicializar tooltips y popovers cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    inicializarTooltips();
    inicializarPopovers();
});
