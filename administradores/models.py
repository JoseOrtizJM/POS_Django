from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Administrador(models.Model):
    email = models.EmailField(unique=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return f"{self.nombre_usuario} ({self.email})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verificar_password(self, raw_password):
        return check_password(raw_password, self.password)
