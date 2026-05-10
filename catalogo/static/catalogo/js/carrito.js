// ==================== CARRITO AJAX ====================

function setCantidadCarrito(url, csrf, cantidad) {
    const fd = new FormData();
    fd.append('cantidad', cantidad);
    fd.append('csrfmiddlewaretoken', csrf);
    return fetch(url, {
        method: 'POST',
        body: fd,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    }).then(r => r.json());
}

function actualizarBadgeCarrito(total) {
    document.querySelectorAll('.carrito-badge').forEach(b => {
        b.textContent = total;
        b.style.display = total > 0 ? '' : 'none';
    });
}

function initCarritoWidgets() {
    document.querySelectorAll('.carrito-widget:not([data-initialized])').forEach(widget => {
        widget.dataset.initialized = '1';
        const stock = parseInt(widget.dataset.stock) || 0;
        const url   = widget.dataset.url;
        const csrf  = widget.dataset.csrf;
        const input = widget.querySelector('.qty-input');
        const minus = widget.querySelector('.qty-minus');
        const plus  = widget.querySelector('.qty-plus');
        if (!input || !url) return;

        let debounce = null;

        function actualizarBotones(v) {
            if (minus) minus.disabled = v <= 0;
            if (plus)  plus.disabled  = v >= stock;
        }

        function enviar(v) {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                setCantidadCarrito(url, csrf, v).then(data => {
                    if (!data.ok) return;
                    input.value = data.cantidad;
                    actualizarBotones(data.cantidad);
                    actualizarBadgeCarrito(data.items_total);
                }).catch(() => {});
            }, 280);
        }

        if (minus) {
            minus.addEventListener('click', () => {
                const v = Math.max(0, (parseInt(input.value) || 0) - 1);
                input.value = v; actualizarBotones(v); enviar(v);
            });
        }
        if (plus) {
            plus.addEventListener('click', () => {
                const v = Math.min(stock, (parseInt(input.value) || 0) + 1);
                input.value = v; actualizarBotones(v); enviar(v);
            });
        }

        input.addEventListener('input', () => {
            const raw = parseInt(input.value);
            if (isNaN(raw)) return;
            const v = Math.max(0, Math.min(stock, raw));
            actualizarBotones(v); enviar(v);
        });

        input.addEventListener('change', () => {
            const v = Math.max(0, Math.min(stock, parseInt(input.value) || 0));
            input.value = v; actualizarBotones(v); enviar(v);
        });

        actualizarBotones(parseInt(input.value) || 0);
    });
}
