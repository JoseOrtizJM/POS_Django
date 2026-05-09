from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from functools import wraps
from .models import Usuario, TarjetaCredito, Carrito, CarritoItem
from .forms import LoginForm, RegistroForm, TarjetaForm, PerfilForm
from api.email import enviar_bienvenida, enviar_confirmacion_pedido


# ==================== DECORADORES ====================

def login_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id') and not request.session.get('admin_id'):
            messages.warning(request, 'Debes iniciar sesión para acceder.')
            return redirect('usuarios:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def solo_usuario(view_func):
    """Solo permite acceso a usuarios clientes (no admins)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.warning(request, 'Inicia sesión como cliente para acceder.')
            return redirect('usuarios:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_usuario(request):
    return Usuario.objects.get(id=request.session['usuario_id'])


def _get_o_crear_carrito(usuario):
    carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


# ==================== AUTENTICACIÓN ====================

def login_view(request):
    if request.session.get('usuario_id') or request.session.get('admin_id'):
        return redirect('catalogo:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identificador = form.cleaned_data['identificador'].strip()
            contrasena = form.cleaned_data['contrasena']

            if '@' in identificador:
                usuario = Usuario.objects.filter(email=identificador.lower(), activo=True).first()
            else:
                usuario = Usuario.objects.filter(nombre_usuario__iexact=identificador, activo=True).first()

            if usuario and usuario.verificar_password(contrasena):
                request.session['usuario_id'] = usuario.id
                request.session['tipo_sesion'] = 'usuario'
                messages.success(request, f'¡Bienvenido, {usuario.get_nombre_corto()}!')
                return redirect('catalogo:dashboard')
            else:
                messages.error(request, 'Credenciales incorrectas. Verifica tu correo/usuario y contraseña.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def registro_view(request):
    if request.session.get('usuario_id') or request.session.get('admin_id'):
        return redirect('catalogo:dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            usuario = Usuario(
                email=d['email'],
                nombre_usuario=d['nombre_usuario'],
                nombre_completo=d['nombre_completo'],
                telefono=d['telefono'],
                direccion=d['direccion'],
                ciudad=d['ciudad'],
                estado_provincia=d['estado_provincia'],
                codigo_postal=d['codigo_postal'],
                pais=d['pais'],
            )
            usuario.set_password(d['contrasena'])
            usuario.save()

            request.session['usuario_id'] = usuario.id
            request.session['tipo_sesion'] = 'usuario'
            enviar_bienvenida(usuario)
            messages.success(request, f'¡Cuenta creada! Bienvenido, {usuario.get_nombre_corto()}.')
            return redirect('catalogo:dashboard')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def logout_view(request):
    request.session.pop('usuario_id', None)
    request.session.pop('admin_id', None)
    request.session.pop('tipo_sesion', None)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('usuarios:login')


# ==================== AJAX — VERIFICACIÓN ÚNICA ====================

@require_GET
def verificar_email(request):
    email = request.GET.get('email', '').lower().strip()
    disponible = not Usuario.objects.filter(email=email).exists()
    return JsonResponse({'disponible': disponible})


@require_GET
def verificar_nombre_usuario(request):
    nombre = request.GET.get('nombre_usuario', '').strip()
    disponible = not Usuario.objects.filter(nombre_usuario__iexact=nombre).exists()
    return JsonResponse({'disponible': disponible})


# ==================== CARRITO ====================

@solo_usuario
def ver_carrito(request):
    usuario = _get_usuario(request)
    carrito = _get_o_crear_carrito(usuario)
    items = carrito.items.select_related('producto', 'producto__categoria').all()
    return render(request, 'usuarios/carrito.html', {
        'carrito': carrito,
        'items': items,
        'titulo': 'Mi Carrito',
    })


@solo_usuario
@require_POST
def agregar_al_carrito(request, producto_id):
    from catalogo.models import Producto
    usuario = _get_usuario(request)
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    if producto.stock == 0:
        messages.warning(request, f'"{producto.nombre}" está agotado.')
        return redirect(request.META.get('HTTP_REFERER', 'catalogo:dashboard'))

    carrito = _get_o_crear_carrito(usuario)
    item, creado = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not creado:
        if item.cantidad < producto.stock:
            item.cantidad += 1
            item.save()
            messages.success(request, f'Cantidad actualizada: {producto.nombre} ×{item.cantidad}.')
        else:
            messages.warning(request, f'No hay más stock disponible de "{producto.nombre}".')
    else:
        messages.success(request, f'"{producto.nombre}" agregado al carrito.')

    return redirect(request.META.get('HTTP_REFERER', 'catalogo:dashboard'))


@solo_usuario
@require_POST
def actualizar_cantidad(request, item_id):
    usuario = _get_usuario(request)
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=usuario)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad = 1

    if cantidad <= 0:
        item.delete()
        messages.success(request, 'Producto eliminado del carrito.')
    elif cantidad <= item.producto.stock:
        item.cantidad = cantidad
        item.save()
    else:
        messages.warning(request, f'Solo hay {item.producto.stock} unidades en stock.')

    return redirect('usuarios:carrito')


@solo_usuario
@require_POST
def eliminar_del_carrito(request, item_id):
    usuario = _get_usuario(request)
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=usuario)
    nombre = item.producto.nombre
    item.delete()
    messages.success(request, f'"{nombre}" eliminado del carrito.')
    return redirect('usuarios:carrito')


# ==================== CHECKOUT ====================

@solo_usuario
def checkout(request):
    usuario = _get_usuario(request)
    carrito = _get_o_crear_carrito(usuario)
    items = carrito.items.select_related('producto').all()

    if not items.exists():
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('usuarios:carrito')

    tarjetas = usuario.tarjetas.all()

    if request.method == 'POST':
        metodo = request.POST.get('metodo_pago')

        if metodo == 'tarjeta':
            tarjeta_id = request.POST.get('tarjeta_id')
            if not tarjeta_id:
                messages.error(request, 'Selecciona una tarjeta de pago.')
                return render(request, 'usuarios/checkout.html', {
                    'carrito': carrito, 'items': items, 'tarjetas': tarjetas,
                })
            tarjeta = get_object_or_404(TarjetaCredito, id=tarjeta_id, usuario=usuario)
            detalle_pago = f"Tarjeta {tarjeta.get_tipo_tarjeta_display()} ****{tarjeta.ultimos_cuatro}"
        elif metodo == 'efectivo':
            detalle_pago = 'Efectivo al momento de entrega'
        else:
            messages.error(request, 'Selecciona un método de pago.')
            return render(request, 'usuarios/checkout.html', {
                'carrito': carrito, 'items': items, 'tarjetas': tarjetas,
            })

        from ventas.models import Venta, VentaItem
        total = carrito.total()

        venta = Venta.objects.create(
            usuario=usuario,
            total=total,
            metodo_pago=metodo,
            detalle_pago=detalle_pago,
        )

        for item in items:
            VentaItem.objects.create(
                venta=venta,
                producto=item.producto,
                nombre_producto=item.producto.nombre,
                precio_unitario=item.producto.precio,
                cantidad=item.cantidad,
                subtotal=item.subtotal(),
            )
            prod = item.producto
            prod.stock = max(0, prod.stock - item.cantidad)
            prod.save()

        carrito.items.all().delete()
        enviar_confirmacion_pedido(usuario, venta)

        messages.success(
            request,
            f'¡Pedido confirmado por ${total:.2f}! Pago: {detalle_pago}. '
            'Nos contactaremos para coordinar la entrega.'
        )
        return redirect('catalogo:dashboard')

    return render(request, 'usuarios/checkout.html', {
        'carrito': carrito,
        'items': items,
        'tarjetas': tarjetas,
        'titulo': 'Confirmar Pedido',
    })


# ==================== PERFIL ====================

@solo_usuario
def mi_perfil(request):
    usuario = _get_usuario(request)

    if request.method == 'POST':
        form = PerfilForm(request.POST, usuario=usuario)
        if form.is_valid():
            d = form.cleaned_data
            usuario.nombre_completo = d['nombre_completo']
            usuario.email = d['email']
            usuario.telefono = d['telefono']
            usuario.direccion = d['direccion']
            usuario.ciudad = d['ciudad']
            usuario.estado_provincia = d['estado_provincia']
            usuario.codigo_postal = d['codigo_postal']
            usuario.pais = d['pais']
            usuario.save()
            messages.success(request, 'Tus datos fueron actualizados correctamente.')
            return redirect('usuarios:perfil')
    else:
        form = PerfilForm(initial={
            'nombre_completo': usuario.nombre_completo,
            'email': usuario.email,
            'telefono': usuario.telefono,
            'direccion': usuario.direccion,
            'ciudad': usuario.ciudad,
            'estado_provincia': usuario.estado_provincia,
            'codigo_postal': usuario.codigo_postal,
            'pais': usuario.pais,
        }, usuario=usuario)

    return render(request, 'usuarios/perfil.html', {
        'form': form,
        'usuario': usuario,
        'titulo': 'Mi Perfil',
    })


# ==================== TARJETAS ====================

@solo_usuario
def mis_tarjetas(request):
    usuario = _get_usuario(request)
    tarjetas = usuario.tarjetas.all()
    return render(request, 'usuarios/mis_tarjetas.html', {
        'tarjetas': tarjetas,
        'titulo': 'Mis Tarjetas',
    })


@solo_usuario
def agregar_tarjeta(request):
    usuario = _get_usuario(request)
    next_url = request.GET.get('next', '') or request.POST.get('next', '')

    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero_tarjeta']
            tipo = form.detectar_tipo(numero)
            es_primera = not usuario.tarjetas.exists()

            tarjeta = TarjetaCredito(
                usuario=usuario,
                nombre_titular=form.cleaned_data['nombre_titular'].upper(),
                ultimos_cuatro=numero[-4:],
                tipo_tarjeta=tipo,
                mes_expiracion=form.cleaned_data['mes_expiracion'],
                anio_expiracion=form.cleaned_data['anio_expiracion'],
                es_predeterminada=es_primera,
            )
            tarjeta.save()
            messages.success(request, f'Tarjeta ****{tarjeta.ultimos_cuatro} guardada correctamente.')

            if next_url == 'checkout':
                return redirect('usuarios:checkout')
            return redirect('usuarios:mis_tarjetas')
    else:
        form = TarjetaForm()

    return render(request, 'usuarios/agregar_tarjeta.html', {
        'form': form,
        'next': next_url,
        'titulo': 'Agregar Tarjeta',
    })


@solo_usuario
@require_POST
def eliminar_tarjeta(request, tarjeta_id):
    usuario = _get_usuario(request)
    tarjeta = get_object_or_404(TarjetaCredito, id=tarjeta_id, usuario=usuario)
    era_predeterminada = tarjeta.es_predeterminada
    tarjeta.delete()

    if era_predeterminada:
        otra = usuario.tarjetas.first()
        if otra:
            otra.es_predeterminada = True
            otra.save()

    messages.success(request, 'Tarjeta eliminada.')
    return redirect('usuarios:mis_tarjetas')


@solo_usuario
@require_POST
def predeterminar_tarjeta(request, tarjeta_id):
    usuario = _get_usuario(request)
    usuario.tarjetas.update(es_predeterminada=False)
    tarjeta = get_object_or_404(TarjetaCredito, id=tarjeta_id, usuario=usuario)
    tarjeta.es_predeterminada = True
    tarjeta.save()
    messages.success(request, f'Tarjeta ****{tarjeta.ultimos_cuatro} establecida como predeterminada.')
    return redirect('usuarios:mis_tarjetas')
