from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
    contexto = {
        'titulo': 'Panel de Administración',
        'total_productos': Producto.objects.count(),
        'total_usuarios': Usuario.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'productos_recientes': Producto.objects.select_related('categoria').order_by('-creado_en')[:5],
    }
    return render(request, 'administradores/panel.html', contexto)


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
            return redirect('administradores:panel')
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
            return redirect('administradores:panel')
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
    return redirect('administradores:panel')


@admin_requerido
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'administradores/listar_usuarios.html', {
        'usuarios': usuarios,
        'titulo': 'Gestión de Usuarios',
    })
