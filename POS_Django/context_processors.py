def auth_context(request):
    from usuarios.models import Usuario, Carrito
    from administradores.models import Administrador

    context = {
        'usuario_actual': None,
        'admin_actual': None,
        'esta_autenticado': False,
        'es_admin': False,
        'items_en_carrito': 0,
    }

    usuario_id = request.session.get('usuario_id')
    admin_id = request.session.get('admin_id')

    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id, activo=True)
            context['usuario_actual'] = usuario
            context['esta_autenticado'] = True

            try:
                context['items_en_carrito'] = usuario.carrito.total_items()
            except Carrito.DoesNotExist:
                pass

        except Usuario.DoesNotExist:
            request.session.pop('usuario_id', None)

    elif admin_id:
        try:
            admin = Administrador.objects.get(id=admin_id, activo=True)
            context['admin_actual'] = admin
            context['esta_autenticado'] = True
            context['es_admin'] = True
        except Administrador.DoesNotExist:
            request.session.pop('admin_id', None)

    return context
