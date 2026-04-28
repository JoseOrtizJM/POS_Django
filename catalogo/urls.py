from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Catálogo
    path('', views.dashboard, name='dashboard'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_categoria'),
    
    # Administración
    path('admin/panel/', views.admin_panel, name='admin_panel'),
    path('admin/crear-producto/', views.crear_producto, name='crear_producto'),
    path('admin/editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin/eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('admin/usuarios/', views.listar_usuarios, name='listar_usuarios'),
]

