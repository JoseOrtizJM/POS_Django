from django.db import models


class Categoria(models.Model):
    """Modelo de Categorías de Productos"""
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

