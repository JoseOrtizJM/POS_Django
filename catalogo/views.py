from django.shortcuts import render, get_object_or_404
from categorias.models import Categoria


def dashboard(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/dashboard.html', {
        'categorias': categorias,
        'titulo': 'Catálogo de Productos',
    })


def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = categoria.productos.filter(activo=True)
    return render(request, 'catalogo/productos_categoria.html', {
        'categoria': categoria,
        'productos': productos,
        'titulo': f'Productos - {categoria.nombre}',
    })
