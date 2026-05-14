from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, date
from functools import wraps
from .models import Administrador
from .forms import LoginAdminForm
from catalogo.models import Producto
from categorias.models import Categoria
from usuarios.models import Usuario


def admin_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            messages.warning(request, 'Debes iniciar sesión como administrador.')
            return redirect('administradores:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.session.get('admin_id'):
        return redirect('administradores:panel')

    if request.method == 'POST':
        form = LoginAdminForm(request.POST)
        if form.is_valid():
            identificador = form.cleaned_data['identificador'].strip()
            contrasena = form.cleaned_data['contrasena']

            admin = None
            if '@' in identificador:
                admin = Administrador.objects.filter(email=identificador.lower(), activo=True).first()
            else:
                admin = Administrador.objects.filter(nombre_usuario__iexact=identificador, activo=True).first()

            if admin and admin.verificar_password(contrasena):
                request.session['admin_id'] = admin.id
                request.session['tipo_sesion'] = 'administrador'
                messages.success(request, f'¡Bienvenido, {admin.nombre_usuario}!')
                return redirect('administradores:panel')
            else:
                messages.error(request, 'Credenciales incorrectas.')
    else:
        form = LoginAdminForm()

    return render(request, 'administradores/login.html', {'form': form})


def logout_view(request):
    request.session.pop('admin_id', None)
    request.session.pop('usuario_id', None)
    request.session.pop('tipo_sesion', None)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('administradores:login')


@admin_requerido
def panel(request):
    from ventas.models import Venta, VentaItem
    hoy = timezone.localdate()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)

    ventas_hoy_qs = Venta.objects.filter(fecha__date=hoy)
    ventas_semana_qs = Venta.objects.filter(fecha__date__gte=inicio_semana)
    ventas_mes_qs = Venta.objects.filter(fecha__date__gte=inicio_mes)

    total_ventas_hoy = ventas_hoy_qs.aggregate(t=Sum('total'))['t'] or 0
    total_ventas_semana = ventas_semana_qs.aggregate(t=Sum('total'))['t'] or 0
    total_ventas_mes = ventas_mes_qs.aggregate(t=Sum('total'))['t'] or 0

    productos_sin_stock = Producto.objects.filter(activo=True, stock=0).count()
    productos_bajo_stock = Producto.objects.filter(activo=True, stock__gt=0, stock__lte=5).count()

    # Ventas por día — últimos 7 días
    labels_7_dias = []
    datos_7_dias = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        total = Venta.objects.filter(fecha__date=dia).aggregate(t=Sum('total'))['t'] or 0
        datos_7_dias.append(float(total))
        labels_7_dias.append(dia.strftime('%d/%m'))

    # Ventas por día — últimos 30 días
    labels_30_dias = []
    datos_30_dias = []
    for i in range(29, -1, -1):
        dia = hoy - timedelta(days=i)
        total = Venta.objects.filter(fecha__date=dia).aggregate(t=Sum('total'))['t'] or 0
        datos_30_dias.append(float(total))
        labels_30_dias.append(dia.strftime('%d/%m'))

    # Métodos de pago del mes
    pago_efectivo = float(ventas_mes_qs.filter(metodo_pago='efectivo').aggregate(t=Sum('total'))['t'] or 0)
    pago_tarjeta = float(ventas_mes_qs.filter(metodo_pago='tarjeta').aggregate(t=Sum('total'))['t'] or 0)

    # Top 5 productos más vendidos del mes
    top_productos = list(
        VentaItem.objects
        .filter(venta__fecha__date__gte=inicio_mes)
        .values('nombre_producto')
        .annotate(total_cantidad=Sum('cantidad'), total_ingresos=Sum('subtotal'))
        .order_by('-total_cantidad')[:5]
    )

    # Ventas recientes
    ventas_recientes = (
        Venta.objects.select_related('usuario')
        .prefetch_related('items')
        .order_by('-fecha')[:10]
    )

    # Productos con stock bajo o agotado
    productos_alerta = (
        Producto.objects.filter(activo=True, stock__lte=5)
        .select_related('categoria')
        .order_by('stock')[:8]
    )

    contexto = {
        'titulo': 'Panel de Administración',
        'hoy': hoy,
        'total_productos': Producto.objects.filter(activo=True).count(),
        'total_productos_inactivos': Producto.objects.filter(activo=False).count(),
        'productos_sin_stock': productos_sin_stock,
        'productos_bajo_stock': productos_bajo_stock,
        'total_usuarios': Usuario.objects.count(),
        'usuarios_activos': Usuario.objects.filter(activo=True).count(),
        'total_categorias': Categoria.objects.count(),
        'ventas_hoy': ventas_hoy_qs.count(),
        'total_ventas_hoy': total_ventas_hoy,
        'ventas_semana': ventas_semana_qs.count(),
        'total_ventas_semana': total_ventas_semana,
        'ventas_mes': ventas_mes_qs.count(),
        'total_ventas_mes': total_ventas_mes,
        'labels_7_dias': labels_7_dias,
        'datos_7_dias': datos_7_dias,
        'labels_30_dias': labels_30_dias,
        'datos_30_dias': datos_30_dias,
        'pago_efectivo': pago_efectivo,
        'pago_tarjeta': pago_tarjeta,
        'top_productos': top_productos,
        'ventas_recientes': ventas_recientes,
        'productos_alerta': productos_alerta,
    }
    return render(request, 'administradores/panel.html', contexto)


# ==================== PRODUCTOS ====================

@admin_requerido
def listar_productos(request):
    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', 'activo')
    stock_filtro = request.GET.get('stock', '')

    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre', 'nombre')

    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(marca__icontains=q))

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if estado == 'activo':
        productos = productos.filter(activo=True)
    elif estado == 'inactivo':
        productos = productos.filter(activo=False)

    if stock_filtro == 'sin_stock':
        productos = productos.filter(stock=0)
    elif stock_filtro == 'bajo':
        productos = productos.filter(stock__gt=0, stock__lte=5)
    elif stock_filtro == 'disponible':
        productos = productos.filter(stock__gt=5)

    categorias = Categoria.objects.order_by('nombre')

    return render(request, 'administradores/listar_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'titulo': 'Gestión de Productos',
        'q': q,
        'categoria_id': categoria_id,
        'estado': estado,
        'stock_filtro': stock_filtro,
    })


@admin_requerido
def crear_producto(request):
    if request.method == 'POST':
        try:
            categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
            producto = Producto(
                nombre=request.POST.get('nombre'),
                marca=request.POST.get('marca'),
                gramaje=request.POST.get('gramaje'),
                categoria=categoria,
                tipo_paquete=request.POST.get('tipo_paquete'),
                piezas_por_paquete=int(request.POST.get('piezas_por_paquete', 1)),
                precio=request.POST.get('precio'),
                stock=int(request.POST.get('stock', 0)),
                descripcion=request.POST.get('descripcion', ''),
            )
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('administradores:listar_productos')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {e}')

    categorias = Categoria.objects.all()
    return render(request, 'administradores/crear_producto.html', {'categorias': categorias})


@admin_requerido
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        try:
            producto.nombre = request.POST.get('nombre')
            producto.marca = request.POST.get('marca')
            producto.gramaje = request.POST.get('gramaje')
            producto.categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
            producto.tipo_paquete = request.POST.get('tipo_paquete')
            producto.piezas_por_paquete = int(request.POST.get('piezas_por_paquete', 1))
            producto.precio = request.POST.get('precio')
            producto.stock = int(request.POST.get('stock', 0))
            producto.descripcion = request.POST.get('descripcion', '')
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado.')
            return redirect('administradores:listar_productos')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    categorias = Categoria.objects.all()
    return render(request, 'administradores/editar_producto.html', {
        'producto': producto,
        'categorias': categorias,
    })


@admin_requerido
@require_POST
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f'Producto "{nombre}" eliminado.')
    return redirect('administradores:listar_productos')


@admin_requerido
@require_POST
def toggle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()
    estado = 'activado' if producto.activo else 'desactivado'
    messages.success(request, f'Producto "{producto.nombre}" {estado}.')
    return redirect('administradores:listar_productos')


# ==================== CATEGORÍAS ====================

@admin_requerido
def listar_categorias(request):
    categorias = Categoria.objects.annotate(
        num_productos=Count('productos'),
        num_activos=Count('productos', filter=Q(productos__activo=True)),
    ).order_by('nombre')
    return render(request, 'administradores/listar_categorias.html', {
        'categorias': categorias,
        'titulo': 'Gestión de Categorías',
    })


@admin_requerido
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            messages.error(request, 'El nombre es requerido.')
        else:
            try:
                cat = Categoria(
                    nombre=nombre,
                    descripcion=request.POST.get('descripcion', ''),
                    icono_emoji=request.POST.get('icono_emoji', '📦') or '📦',
                )
                if 'imagen' in request.FILES:
                    cat.imagen = request.FILES['imagen']
                cat.save()
                messages.success(request, f'Categoría "{nombre}" creada.')
                return redirect('administradores:listar_categorias')
            except Exception as e:
                messages.error(request, f'Error: {e}')
    return render(request, 'administradores/crear_categoria.html', {'titulo': 'Nueva Categoría'})


@admin_requerido
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            messages.error(request, 'El nombre es requerido.')
        else:
            try:
                categoria.nombre = nombre
                categoria.descripcion = request.POST.get('descripcion', '')
                categoria.icono_emoji = request.POST.get('icono_emoji', '📦') or '📦'
                if 'imagen' in request.FILES:
                    categoria.imagen = request.FILES['imagen']
                categoria.save()
                messages.success(request, f'Categoría "{nombre}" actualizada.')
                return redirect('administradores:listar_categorias')
            except Exception as e:
                messages.error(request, f'Error: {e}')
    return render(request, 'administradores/editar_categoria.html', {
        'categoria': categoria,
        'titulo': 'Editar Categoría',
    })


@admin_requerido
@require_POST
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    nombre = categoria.nombre
    num_productos = categoria.productos.count()
    categoria.delete()
    messages.success(request, f'Categoría "{nombre}" y {num_productos} producto(s) eliminados.')
    return redirect('administradores:listar_categorias')


# ==================== USUARIOS ====================

@admin_requerido
def listar_usuarios(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    usuarios = Usuario.objects.annotate(
        num_ventas=Count('ventas'),
        total_gastado=Sum('ventas__total'),
    ).order_by('-creado_en')

    if q:
        usuarios = usuarios.filter(
            Q(nombre_completo__icontains=q) |
            Q(nombre_usuario__icontains=q) |
            Q(email__icontains=q)
        )

    if estado == 'activo':
        usuarios = usuarios.filter(activo=True)
    elif estado == 'inactivo':
        usuarios = usuarios.filter(activo=False)

    return render(request, 'administradores/listar_usuarios.html', {
        'usuarios': usuarios,
        'titulo': 'Gestión de Usuarios',
        'q': q,
        'estado': estado,
    })


@admin_requerido
@require_POST
def toggle_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.activo = not usuario.activo
    usuario.save()
    estado = 'activado' if usuario.activo else 'desactivado'
    messages.success(request, f'Usuario "{usuario.nombre_usuario}" {estado}.')
    return redirect('administradores:listar_usuarios')


# ==================== VENTAS ====================

@admin_requerido
def ventas_dia(request):
    from ventas.models import Venta
    hoy = timezone.localdate()
    ventas = Venta.objects.filter(fecha__date=hoy).select_related('usuario').prefetch_related('items')
    total_dia = ventas.aggregate(t=Sum('total'))['t'] or 0
    return render(request, 'administradores/ventas_dia.html', {
        'ventas': ventas,
        'total_dia': total_dia,
        'hoy': hoy,
        'titulo': 'Ventas del Día',
    })


@admin_requerido
def ventas_reporte(request):
    from ventas.models import Venta, VentaItem
    hoy = timezone.localdate()

    periodo = request.GET.get('periodo', 'hoy')
    fecha_desde_str = request.GET.get('desde', '')
    fecha_hasta_str = request.GET.get('hasta', '')

    if periodo == 'semana':
        fecha_desde = hoy - timedelta(days=hoy.weekday())
        fecha_hasta = hoy
        titulo_periodo = 'Esta semana'
    elif periodo == 'mes':
        fecha_desde = hoy.replace(day=1)
        fecha_hasta = hoy
        titulo_periodo = 'Este mes'
    elif periodo == 'personalizado' and fecha_desde_str and fecha_hasta_str:
        try:
            fecha_desde = date.fromisoformat(fecha_desde_str)
            fecha_hasta = date.fromisoformat(fecha_hasta_str)
            if fecha_desde > fecha_hasta:
                fecha_desde, fecha_hasta = fecha_hasta, fecha_desde
            titulo_periodo = f'{fecha_desde.strftime("%d/%m/%Y")} — {fecha_hasta.strftime("%d/%m/%Y")}'
        except ValueError:
            fecha_desde = hoy
            fecha_hasta = hoy
            titulo_periodo = 'Hoy'
            periodo = 'hoy'
    else:
        fecha_desde = hoy
        fecha_hasta = hoy
        titulo_periodo = 'Hoy'
        periodo = 'hoy'

    ventas_qs = (
        Venta.objects
        .filter(fecha__date__gte=fecha_desde, fecha__date__lte=fecha_hasta)
        .select_related('usuario')
        .prefetch_related('items')
        .order_by('-fecha')
    )

    total_periodo = ventas_qs.aggregate(t=Sum('total'))['t'] or 0
    ticket_promedio = ventas_qs.aggregate(a=Avg('total'))['a'] or 0
    pago_efectivo_monto = float(ventas_qs.filter(metodo_pago='efectivo').aggregate(t=Sum('total'))['t'] or 0)
    pago_tarjeta_monto = float(ventas_qs.filter(metodo_pago='tarjeta').aggregate(t=Sum('total'))['t'] or 0)
    ventas_efectivo_count = ventas_qs.filter(metodo_pago='efectivo').count()
    ventas_tarjeta_count = ventas_qs.filter(metodo_pago='tarjeta').count()

    # Gráfica: ventas por día en el período
    dias_total = (fecha_hasta - fecha_desde).days + 1
    labels_periodo = []
    datos_periodo = []
    for i in range(dias_total):
        dia = fecha_desde + timedelta(days=i)
        total = Venta.objects.filter(fecha__date=dia).aggregate(t=Sum('total'))['t'] or 0
        datos_periodo.append(float(total))
        labels_periodo.append(dia.strftime('%d/%m'))

    # Top 10 productos del período
    top_productos = list(
        VentaItem.objects
        .filter(venta__fecha__date__gte=fecha_desde, venta__fecha__date__lte=fecha_hasta)
        .values('nombre_producto')
        .annotate(total_cantidad=Sum('cantidad'), total_ingresos=Sum('subtotal'))
        .order_by('-total_ingresos')[:10]
    )

    contexto = {
        'titulo': 'Reporte de Ventas',
        'hoy': hoy,
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'fecha_desde_str': fecha_desde.isoformat(),
        'fecha_hasta_str': fecha_hasta.isoformat(),
        'ventas': ventas_qs,
        'total_ventas': ventas_qs.count(),
        'total_periodo': total_periodo,
        'ticket_promedio': ticket_promedio,
        'pago_efectivo_monto': pago_efectivo_monto,
        'pago_tarjeta_monto': pago_tarjeta_monto,
        'ventas_efectivo_count': ventas_efectivo_count,
        'ventas_tarjeta_count': ventas_tarjeta_count,
        'labels_periodo': labels_periodo,
        'datos_periodo': datos_periodo,
        'top_productos': top_productos,
    }
    return render(request, 'administradores/ventas_reporte.html', contexto)


@admin_requerido
def detalle_venta(request, venta_id):
    from ventas.models import Venta
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'administradores/detalle_venta.html', {
        'venta': venta,
        'titulo': f'Detalle — Venta #{venta.id}',
    })


# ==================== PERFIL ====================

@admin_requerido
def perfil_admin(request):
    admin = get_object_or_404(Administrador, id=request.session['admin_id'])
    from ventas.models import Venta
    from django.db.models import Sum

    total_productos = Producto.objects.count()
    total_usuarios = Usuario.objects.count()
    total_ventas = Venta.objects.count()
    total_ingresos = Venta.objects.aggregate(t=Sum('total'))['t'] or 0

    error_pw = None
    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        if accion == 'cambiar_password':
            actual = request.POST.get('password_actual', '')
            nueva = request.POST.get('password_nueva', '')
            confirmar = request.POST.get('password_confirmar', '')

            if not admin.verificar_password(actual):
                error_pw = 'La contraseña actual es incorrecta.'
            elif len(nueva) < 6:
                error_pw = 'La nueva contraseña debe tener al menos 6 caracteres.'
            elif nueva != confirmar:
                error_pw = 'Las contraseñas nuevas no coinciden.'
            else:
                admin.set_password(nueva)
                admin.save()
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('administradores:perfil')

        elif accion == 'actualizar_datos':
            nuevo_email = request.POST.get('email', '').strip().lower()
            nuevo_usuario = request.POST.get('nombre_usuario', '').strip()

            if not nuevo_email or not nuevo_usuario:
                messages.error(request, 'Email y nombre de usuario son requeridos.')
            elif Administrador.objects.exclude(id=admin.id).filter(email=nuevo_email).exists():
                messages.error(request, 'Ese email ya está en uso.')
            elif Administrador.objects.exclude(id=admin.id).filter(nombre_usuario__iexact=nuevo_usuario).exists():
                messages.error(request, 'Ese nombre de usuario ya está en uso.')
            else:
                admin.email = nuevo_email
                admin.nombre_usuario = nuevo_usuario
                admin.save()
                messages.success(request, 'Datos actualizados correctamente.')
                return redirect('administradores:perfil')

    return render(request, 'administradores/perfil.html', {
        'titulo': 'Mi Perfil',
        'admin': admin,
        'total_productos': total_productos,
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'total_ingresos': total_ingresos,
        'error_pw': error_pw,
    })
