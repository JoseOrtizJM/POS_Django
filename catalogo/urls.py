from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_categoria'),
    path('buscar/', views.buscar_productos, name='buscar'),
]
