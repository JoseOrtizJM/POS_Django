from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
from .models import Categoria, Producto, UsuarioPOS
from .forms import LoginForm, RegistroForm


# ==================== VISTAS DE AUTENTICACIÓN ====================

def login_view(request):
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('catalogo:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            
            # Buscar usuario por correo (email)
            try:
                user = User.objects.get(email=correo)
                user_auth = authenticate(request, username=user.username, password=contrasena)
                
                if user_auth is not None:
                    login(request, user_auth)
                    messages.success(request, '¡Bienvenido! Sesión iniciada correctamente.')
                    return redirect('catalogo:dashboard')
                else:
                    messages.error(request, 'Correo o contraseña incorrectos')
            except User.DoesNotExist:
                messages.error(request, 'Correo o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'catalogo/login.html', {'form': form})


def registro_view(request):
    """Vista para registrarse"""
    if request.user.is_authenticated:
        return redirect('catalogo:dashboard')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                correo = form.cleaned_data['correo']
                contrasena = form.cleaned_data['contrasena']
                
                # Crear usuario
                username = correo.split('@')[0]  # Usar la parte del email como username
                # Si el username ya existe, agregar un número
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=correo,
                    password=contrasena
                )
                
                # Crear perfil POS del usuario
                UsuarioPOS.objects.create(
                    user=user,
                    rol='usuario'
                )
                
                # Autenticar e iniciar sesión
                user_auth = authenticate(request, username=user.username, password=contrasena)
                login(request, user_auth)
                
                messages.success(request, '¡Cuenta creada exitosamente! Bienvenido.')
                return redirect('catalogo:dashboard')
            
            except IntegrityError:
                messages.error(request, 'Error al crear la cuenta. Por favor intenta de nuevo.')
    else:
        form = RegistroForm()
    
    return render(request, 'catalogo/registro.html', {'form': form})


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('catalogo:login')


# ==================== VISTAS DEL CATÁLOGO ====================

def dashboard(request):
    """Vista del dashboard con todas las categorías"""
    categorias = Categoria.objects.all()
    contexto = {
        'categorias': categorias,
        'titulo': 'Dashboard - Catálogo de Productos'
    }
    return render(request, 'catalogo/dashboard.html', contexto)


def productos_por_categoria(request, categoria_id):
    """Vista que lista los productos de una categoría específica"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = categoria.productos.filter(activo=True)
    
    contexto = {
        'categoria': categoria,
        'productos': productos,
        'titulo': f'Productos - {categoria.nombre}'
    }
    return render(request, 'catalogo/productos_categoria.html', contexto)


# ==================== VISTAS DE ADMINISTRACIÓN ====================

@login_required(login_url='catalogo:login')
def require_admin(view_func):
    """Decorador para verificar que el usuario sea administrador"""
    def wrapped_view(request, *args, **kwargs):
        try:
            if request.user.pos_usuario.es_admin():
                return view_func(request, *args, **kwargs)
        except UsuarioPOS.DoesNotExist:
            pass
        return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    return wrapped_view


@login_required(login_url='catalogo:login')
def admin_panel(request):
    """Panel de administración"""
    try:
        if not request.user.pos_usuario.es_admin():
            return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    except UsuarioPOS.DoesNotExist:
        return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    
    usuarios = User.objects.all()
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    contexto = {
        'usuarios': usuarios,
        'productos': productos,
        'categorias': categorias,
        'total_usuarios': usuarios.count(),
        'total_productos': productos.count(),
        'total_categorias': categorias.count(),
        'titulo': 'Panel de Administración'
    }
    return render(request, 'catalogo/admin_panel.html', contexto)


@login_required(login_url='catalogo:login')
def crear_producto(request):
    """Vista para crear un nuevo producto"""
    try:
        if not request.user.pos_usuario.es_admin():
            return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    except UsuarioPOS.DoesNotExist:
        return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    
    if request.method == 'POST':
        try:
            categoria = Categoria.objects.get(id=request.POST.get('categoria'))
            producto = Producto(
                nombre=request.POST.get('nombre'),
                marca=request.POST.get('marca'),
                gramaje=request.POST.get('gramaje'),
                categoria=categoria,
                tipo_paquete=request.POST.get('tipo_paquete'),
                piezas_por_paquete=request.POST.get('piezas_por_paquete'),
                precio=request.POST.get('precio'),
                stock=request.POST.get('stock'),
                descripcion=request.POST.get('descripcion', ''),
                activo=True
            )
            
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            
            producto.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('catalogo:admin_panel')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/crear_producto.html', {'categorias': categorias})


@login_required(login_url='catalogo:login')
def editar_producto(request, producto_id):
    """Vista para editar un producto"""
    try:
        if not request.user.pos_usuario.es_admin():
            return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    except UsuarioPOS.DoesNotExist:
        return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        try:
            producto.nombre = request.POST.get('nombre')
            producto.marca = request.POST.get('marca')
            producto.gramaje = request.POST.get('gramaje')
            producto.categoria = Categoria.objects.get(id=request.POST.get('categoria'))
            producto.tipo_paquete = request.POST.get('tipo_paquete')
            producto.piezas_por_paquete = request.POST.get('piezas_por_paquete')
            producto.precio = request.POST.get('precio')
            producto.stock = request.POST.get('stock')
            producto.descripcion = request.POST.get('descripcion', '')
            
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('catalogo:admin_panel')
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/editar_producto.html', {
        'producto': producto,
        'categorias': categorias
    })


@login_required(login_url='catalogo:login')
@require_http_methods(["POST"])
def eliminar_producto(request, producto_id):
    """Vista para eliminar un producto"""
    try:
        if not request.user.pos_usuario.es_admin():
            return JsonResponse({'error': 'No tienes permiso'}, status=403)
    except UsuarioPOS.DoesNotExist:
        return JsonResponse({'error': 'No tienes permiso'}, status=403)
    
    producto = get_object_or_404(Producto, id=producto_id)
    nombre = producto.nombre
    producto.delete()
    
    messages.success(request, f'Producto "{nombre}" eliminado exitosamente')
    return redirect('catalogo:admin_panel')


@login_required(login_url='catalogo:login')
def listar_usuarios(request):
    """Vista para ver la lista de usuarios registrados"""
    try:
        if not request.user.pos_usuario.es_admin():
            return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    except UsuarioPOS.DoesNotExist:
        return HttpResponseForbidden('No tienes permiso para acceder a esta página')
    
    usuarios = UsuarioPOS.objects.all().select_related('user')
    
    return render(request, 'catalogo/listar_usuarios.html', {
        'usuarios': usuarios,
        'titulo': 'Gestión de Usuarios'
    })

