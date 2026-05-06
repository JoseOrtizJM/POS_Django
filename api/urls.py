from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # ── Catálogo público ──────────────────────────────────────
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/<int:pk>/', views.detalle_categoria, name='detalle-categoria'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle-producto'),

    # ── Autenticación de clientes ─────────────────────────────
    path('auth/registro/', views.registro_usuario, name='registro'),
    path('auth/login/', views.login_usuario, name='login'),
    path('auth/logout/', views.logout_usuario, name='logout'),

    # ── Autenticación de administradores ─────────────────────
    path('auth/admin/login/', views.login_admin, name='login-admin'),

    # ── Perfil ────────────────────────────────────────────────
    path('perfil/', views.perfil_usuario, name='perfil'),

    # ── Carrito ───────────────────────────────────────────────
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/', views.agregar_item, name='agregar-item'),
    path('carrito/items/<int:item_id>/', views.actualizar_item, name='actualizar-item'),
    path('carrito/items/<int:item_id>/eliminar/', views.eliminar_item, name='eliminar-item'),

    # ── Checkout ──────────────────────────────────────────────
    path('checkout/', views.checkout, name='checkout'),

    # ── Historial de ventas del cliente ───────────────────────
    path('ventas/', views.mis_ventas, name='mis-ventas'),
    path('ventas/<int:pk>/', views.detalle_venta, name='detalle-venta'),

    # ── Panel de administrador ────────────────────────────────
    path('admin/resumen/', views.admin_resumen, name='admin-resumen'),
    path('admin/ventas/', views.admin_lista_ventas, name='admin-ventas'),
    path('admin/usuarios/', views.admin_lista_usuarios, name='admin-usuarios'),
    path('admin/usuarios/<int:pk>/toggle/', views.admin_toggle_usuario, name='admin-toggle-usuario'),
    path('admin/productos/', views.admin_lista_productos, name='admin-productos'),
    path('admin/productos/<int:pk>/toggle/', views.admin_toggle_producto, name='admin-toggle-producto'),
]
