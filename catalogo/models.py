from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validar_email(email):
    """Valida que el email tenga un formato correcto"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        raise ValidationError('Correo electrónico inválido')


class UsuarioPOS(models.Model):
    """Modelo personalizado de usuario para el POS"""
    ROLES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario Regular'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pos_usuario')
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')
    correo_validado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Usuarios POS'
    
    def __str__(self):
        return f"{self.user.email} - {self.get_rol_display()}"
    
    def es_admin(self):
        return self.rol == 'admin'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    icono_emoji = models.CharField(max_length=10, default='📦')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100)
    gramaje = models.CharField(max_length=50)  # "600ml", "1kg", "250g", etc.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    tipo_paquete = models.CharField(max_length=50)  # "Paquete", "Caja", "Bulto"
    piezas_por_paquete = models.IntegerField()  # Cantidad de unidades por paquete
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio en pesos mexicanos
    stock = models.IntegerField(default=0)  # Stock en paquetes
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.gramaje}"
