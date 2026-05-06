from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenAPIAuthentication(BaseAuthentication):
    """
    Autenticación de clientes por token.
    Header esperado: Authorization: Token <key>
    Asigna request.user = instancia de Usuario.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Token '):
            return None

        token_key = auth_header.split(' ', 1)[1].strip()
        if not token_key:
            raise AuthenticationFailed('Token vacío.')

        from .models import TokenAPI
        try:
            token = TokenAPI.objects.select_related('usuario').get(key=token_key)
        except TokenAPI.DoesNotExist:
            raise AuthenticationFailed('Token inválido o expirado.')

        if not token.usuario.activo:
            raise AuthenticationFailed('Esta cuenta está desactivada.')

        return (token.usuario, token)

    def authenticate_header(self, request):
        return 'Token'


class AdminTokenAPIAuthentication(BaseAuthentication):
    """
    Autenticación de administradores por token.
    Header esperado: Authorization: Admin <key>
    Asigna request.user = instancia de Administrador.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Admin '):
            return None

        token_key = auth_header.split(' ', 1)[1].strip()
        if not token_key:
            raise AuthenticationFailed('Token de admin vacío.')

        from .models import TokenAPIAdmin
        try:
            token = TokenAPIAdmin.objects.select_related('administrador').get(key=token_key)
        except TokenAPIAdmin.DoesNotExist:
            raise AuthenticationFailed('Token de administrador inválido o expirado.')

        if not token.administrador.activo:
            raise AuthenticationFailed('Esta cuenta de administrador está desactivada.')

        return (token.administrador, token)

    def authenticate_header(self, request):
        return 'Admin'
