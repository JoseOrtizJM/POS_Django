import binascii
import os
from django.db import models


def _generar_key():
    return binascii.hexlify(os.urandom(20)).decode()


class TokenAPI(models.Model):
    """Token de autenticación para clientes (Usuario)."""
    key = models.CharField(max_length=40, primary_key=True)
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='token_api',
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token API (Usuario)'
        verbose_name_plural = 'Tokens API (Usuarios)'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = _generar_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token de {self.usuario.nombre_usuario}"


class TokenAPIAdmin(models.Model):
    """Token de autenticación para administradores."""
    key = models.CharField(max_length=40, primary_key=True)
    administrador = models.OneToOneField(
        'administradores.Administrador',
        on_delete=models.CASCADE,
        related_name='token_api',
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token API (Admin)'
        verbose_name_plural = 'Tokens API (Admins)'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = _generar_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token admin de {self.administrador.nombre_usuario}"
