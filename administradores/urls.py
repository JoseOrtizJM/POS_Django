from django.urls import path
from . import views

app_name = 'administradores'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel, name='panel'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
]
