from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def enviar_bienvenida(usuario):
    """Envía correo de bienvenida al registrarse. Falla silenciosamente."""
    if not getattr(settings, 'EMAIL_NOTIFICACIONES_ENABLED', False):
        return
    try:
        send_mail(
            subject='Bienvenido a Mayorista',
            message=(
                f"Hola {usuario.get_nombre_corto()},\n\n"
                f"Tu cuenta fue creada exitosamente.\n"
                f"Usuario: {usuario.nombre_usuario}\n"
                f"Correo: {usuario.email}\n\n"
                f"Ya puedes explorar nuestro catalogo y realizar pedidos.\n\n"
                f"— Equipo Mayorista"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=True,
        )
    except Exception:
        pass


def enviar_confirmacion_pedido(usuario, venta):
    """Envía confirmación de compra tras el checkout. Falla silenciosamente."""
    if not getattr(settings, 'EMAIL_NOTIFICACIONES_ENABLED', False):
        return
    try:
        lineas_items = '\n'.join(
            f"  - {item.nombre_producto} x{item.cantidad}  ${item.subtotal:.2f}"
            for item in venta.items.all()
        )
        fecha = timezone.localtime(venta.fecha).strftime('%d/%m/%Y %H:%M')
        send_mail(
            subject=f'Pedido #{venta.id} confirmado — ${venta.total:.2f} MXN',
            message=(
                f"Hola {usuario.get_nombre_corto()},\n\n"
                f"Tu pedido fue procesado exitosamente.\n\n"
                f"Pedido: #{venta.id}\n"
                f"Fecha:  {fecha}\n"
                f"Pago:   {venta.get_metodo_pago_display()}\n\n"
                f"Productos:\n{lineas_items}\n\n"
                f"Total: ${venta.total:.2f} MXN\n\n"
                f"— Equipo Mayorista"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=True,
        )
    except Exception:
        pass
