from rest_framework.permissions import BasePermission
from usuarios.models import Usuario
from administradores.models import Administrador


class IsUsuarioAuthenticated(BasePermission):
    """Solo clientes autenticados con su token (Authorization: Token <key>)."""
    message = 'Se requiere autenticación como cliente.'

    def has_permission(self, request, view):
        return isinstance(request.user, Usuario) and request.user.activo


class IsAdminAuthenticated(BasePermission):
    """Solo administradores autenticados con su token (Authorization: Admin <key>)."""
    message = 'Se requiere autenticación de administrador.'

    def has_permission(self, request, view):
        return isinstance(request.user, Administrador) and request.user.activo
