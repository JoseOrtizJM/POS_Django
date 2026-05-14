from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from categorias.models import Categoria
from .models import Producto


def dashboard(request):
    if request.session.get('admin_id'):
        return redirect('administradores:panel')
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/dashboard.html', {
        'categorias': categorias,
        'titulo': 'Catálogo de Productos',
    })


def buscar_productos(request):
    from django.urls import reverse
    q = request.GET.get('q', '').strip()
    autenticado = bool(request.session.get('usuario_id'))
    es_admin = bool(request.session.get('admin_id'))

    if not q or len(q) < 2:
        return JsonResponse({'productos': [], 'autenticado': autenticado, 'es_admin': es_admin})

    productos = (
        Producto.objects
        .filter(activo=True)
        .filter(Q(nombre__icontains=q) | Q(marca__icontains=q))
        .select_related('categoria')
        .order_by('nombre')[:30]
    )

    cantidades_carrito = {}
    if autenticado:
        from usuarios.models import Carrito
        try:
            carrito = Carrito.objects.get(usuario_id=request.session['usuario_id'])
            cantidades_carrito = {item.producto_id: item.cantidad for item in carrito.items.all()}
        except Carrito.DoesNotExist:
            pass

    resultado = []
    for p in productos:
        resultado.append({
            'id': p.id,
            'nombre': p.nombre,
            'marca': p.marca,
            'gramaje': p.gramaje,
            'precio': str(p.precio),
            'tipo_paquete': p.tipo_paquete,
            'piezas_por_paquete': p.piezas_por_paquete,
            'stock': p.stock,
            'imagen_url': p.imagen.url if p.imagen else None,
            'categoria_id': p.categoria_id,
            'categoria_nombre': p.categoria.nombre,
            'categoria_emoji': p.categoria.icono_emoji,
            'cantidad_en_carrito': cantidades_carrito.get(p.id, 0),
            'url_set_cantidad': reverse('usuarios:set_cantidad', args=[p.id]),
        })

    return JsonResponse({'productos': resultado, 'autenticado': autenticado, 'es_admin': es_admin})


def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = list(categoria.productos.filter(activo=True))

    cantidades_carrito = {}
    if request.session.get('usuario_id'):
        from usuarios.models import Carrito
        try:
            carrito = Carrito.objects.get(usuario_id=request.session['usuario_id'])
            cantidades_carrito = {item.producto_id: item.cantidad for item in carrito.items.all()}
        except Carrito.DoesNotExist:
            pass

    for p in productos:
        p.cantidad_en_carrito = cantidades_carrito.get(p.id, 0)

    return render(request, 'catalogo/productos_categoria.html', {
        'categoria': categoria,
        'productos': productos,
        'titulo': f'Productos - {categoria.nombre}',
    })
