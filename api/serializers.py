from rest_framework import serializers
from categorias.models import Categoria
from catalogo.models import Producto
from usuarios.models import Usuario, Carrito, CarritoItem
from ventas.models import Venta, VentaItem


# ──────────────────────────────────────────────
# CATEGORÍAS
# ──────────────────────────────────────────────

class CategoriaSerializer(serializers.ModelSerializer):
    total_productos = serializers.SerializerMethodField()
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'icono_emoji', 'imagen', 'total_productos']

    def get_total_productos(self, obj):
        return obj.productos.filter(activo=True).count()

    def get_imagen(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return None


# ──────────────────────────────────────────────
# PRODUCTOS
# ──────────────────────────────────────────────

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_emoji = serializers.CharField(source='categoria.icono_emoji', read_only=True)
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'marca', 'gramaje',
            'categoria', 'categoria_nombre', 'categoria_emoji',
            'tipo_paquete', 'piezas_por_paquete',
            'precio', 'stock', 'descripcion', 'imagen',
        ]

    def get_imagen(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return None


# ──────────────────────────────────────────────
# CARRITO
# ──────────────────────────────────────────────

class CarritoItemSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_marca = serializers.CharField(source='producto.marca', read_only=True)
    precio_unitario = serializers.DecimalField(
        source='producto.precio', max_digits=10, decimal_places=2, read_only=True
    )
    stock_disponible = serializers.IntegerField(source='producto.stock', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CarritoItem
        fields = [
            'id', 'producto', 'producto_nombre', 'producto_marca',
            'precio_unitario', 'stock_disponible', 'cantidad', 'subtotal',
        ]

    def get_subtotal(self, obj):
        return float(obj.subtotal())


class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'items', 'total', 'total_items', 'actualizado_en']

    def get_total(self, obj):
        return float(obj.total())

    def get_total_items(self, obj):
        return obj.total_items()


# ──────────────────────────────────────────────
# VENTAS
# ──────────────────────────────────────────────

class VentaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaItem
        fields = ['id', 'nombre_producto', 'precio_unitario', 'cantidad', 'subtotal']


class VentaSerializer(serializers.ModelSerializer):
    items = VentaItemSerializer(many=True, read_only=True)
    metodo_pago_display = serializers.CharField(source='get_metodo_pago_display', read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'total', 'metodo_pago', 'metodo_pago_display', 'detalle_pago', 'items']


# ──────────────────────────────────────────────
# USUARIO (perfil)
# ──────────────────────────────────────────────

class UsuarioPerfilSerializer(serializers.ModelSerializer):
    pais_display = serializers.CharField(source='get_pais_display', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'nombre_usuario', 'nombre_completo',
            'telefono', 'direccion', 'ciudad', 'estado_provincia',
            'codigo_postal', 'pais', 'pais_display', 'creado_en',
        ]
        read_only_fields = ['id', 'email', 'nombre_usuario', 'creado_en']


# ──────────────────────────────────────────────
# REGISTRO / LOGIN (entrada de datos)
# ──────────────────────────────────────────────

class RegistroSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nombre_usuario = serializers.CharField(max_length=50)
    nombre_completo = serializers.CharField(max_length=150)
    telefono = serializers.CharField(max_length=20)
    direccion = serializers.CharField(max_length=255)
    ciudad = serializers.CharField(max_length=100)
    estado_provincia = serializers.CharField(max_length=100)
    codigo_postal = serializers.CharField(max_length=20)
    pais = serializers.ChoiceField(choices=Usuario.PAISES, default='MX')
    contrasena = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):
        if Usuario.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('Este correo ya está registrado.')
        return value.lower()

    def validate_nombre_usuario(self, value):
        if Usuario.objects.filter(nombre_usuario__iexact=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya existe.')
        return value


class LoginSerializer(serializers.Serializer):
    identificador = serializers.CharField(help_text='Email o nombre de usuario')
    contrasena = serializers.CharField(write_only=True)


class AgregarItemSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1, default=1)


class ActualizarCantidadSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=0)


class CheckoutSerializer(serializers.Serializer):
    METODOS = [('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta')]
    metodo_pago = serializers.ChoiceField(choices=METODOS)
    tarjeta_id = serializers.IntegerField(required=False, allow_null=True)
