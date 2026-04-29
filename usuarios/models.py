from django.db import models
from django.contrib.auth.hashers import make_password, check_password


def validar_telefono(telefono):
    import re
    from django.core.exceptions import ValidationError
    patron = r'^\+?1?\d{9,15}$'
    if not re.match(patron, telefono.replace(' ', '').replace('-', '')):
        raise ValidationError('Número de teléfono inválido (ej: 5512345678)')


class Usuario(models.Model):
    PAISES = [
        ('MX', 'México'),
        ('US', 'Estados Unidos'),
        ('CA', 'Canadá'),
        ('ES', 'España'),
        ('AR', 'Argentina'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('PE', 'Perú'),
    ]

    email = models.EmailField(unique=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    nombre_completo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, validators=[validar_telefono])

    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=2, choices=PAISES, default='MX')

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verificar_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_nombre_corto(self):
        partes = self.nombre_completo.split()
        return partes[0] if partes else self.nombre_usuario


class TarjetaCredito(models.Model):
    TIPOS = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('otro', 'Otra'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tarjetas')
    nombre_titular = models.CharField(max_length=100)
    ultimos_cuatro = models.CharField(max_length=4)
    tipo_tarjeta = models.CharField(max_length=20, choices=TIPOS, default='otro')
    mes_expiracion = models.CharField(max_length=2)
    anio_expiracion = models.CharField(max_length=4)
    es_predeterminada = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-es_predeterminada', '-creado_en']
        verbose_name_plural = 'Tarjetas de crédito'

    def __str__(self):
        return f"{self.get_tipo_tarjeta_display()} ****{self.ultimos_cuatro} ({self.nombre_titular})"


class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carrito')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.cantidad for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.nombre_usuario}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('catalogo.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'producto')

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
