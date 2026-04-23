from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Categoria, Producto


def dashboard(request):
    """Vista del dashboard con todas las categorías"""
    categorias = Categoria.objects.all()
    contexto = {
        'categorias': categorias,
        'titulo': 'Dashboard - Catálogo de Productos'
    }
    return render(request, 'catalogo/dashboard.html', contexto)


def productos_por_categoria(request, categoria_id):
    """Vista que lista los productos de una categoría específica"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = categoria.productos.filter(activo=True)
    
    contexto = {
        'categoria': categoria,
        'productos': productos,
        'titulo': f'Productos - {categoria.nombre}'
    }
    return render(request, 'catalogo/productos_categoria.html', contexto)
