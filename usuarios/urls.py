from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Perfil
    path('perfil/', views.mi_perfil, name='perfil'),

    # AJAX
    path('verificar-email/', views.verificar_email, name='verificar_email'),
    path('verificar-usuario/', views.verificar_nombre_usuario, name='verificar_nombre_usuario'),

    # Carrito
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Tarjetas
    path('tarjetas/', views.mis_tarjetas, name='mis_tarjetas'),
    path('tarjetas/agregar/', views.agregar_tarjeta, name='agregar_tarjeta'),
    path('tarjetas/eliminar/<int:tarjeta_id>/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
    path('tarjetas/predeterminar/<int:tarjeta_id>/', views.predeterminar_tarjeta, name='predeterminar_tarjeta'),
]
