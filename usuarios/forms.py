from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario
import re
from datetime import date


class RegistroForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
            'id': 'id_email',
        })
    )
    nombre_usuario = forms.CharField(
        label='Nombre de Usuario',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario123',
            'id': 'id_nombre_usuario',
        }),
        help_text='Solo letras, números y guiones bajos. Debe ser único.'
    )
    nombre_completo = forms.CharField(
        label='Nombre Completo',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Pérez López'})
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5512345678'})
    )
    direccion = forms.CharField(
        label='Dirección',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle Ejemplo 123, Col. Centro'})
    )
    ciudad = forms.CharField(
        label='Ciudad',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de México'})
    )
    estado_provincia = forms.CharField(
        label='Estado / Provincia',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CDMX'})
    )
    codigo_postal = forms.CharField(
        label='Código Postal',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '06600'})
    )
    pais = forms.ChoiceField(
        label='País',
        choices=Usuario.PAISES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    contrasena = forms.CharField(
        label='Contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
            'id': 'id_contrasena',
        }),
        help_text='Mínimo 8 caracteres, una mayúscula y un número.'
    )
    contrasena_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'id': 'id_contrasena_confirm',
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Este correo ya está registrado.')
        return email

    def clean_nombre_usuario(self):
        nombre = self.cleaned_data['nombre_usuario'].strip()
        if not re.match(r'^[a-zA-Z0-9_]+$', nombre):
            raise ValidationError('Solo se permiten letras, números y guiones bajos.')
        if Usuario.objects.filter(nombre_usuario__iexact=nombre).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        limpio = telefono.replace(' ', '').replace('-', '')
        if not re.match(r'^\+?1?\d{9,15}$', limpio):
            raise ValidationError('Número de teléfono inválido (ej: 5512345678).')
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('contrasena')
        p2 = cleaned_data.get('contrasena_confirm')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class LoginForm(forms.Form):
    identificador = forms.CharField(
        label='Correo o Nombre de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com  o  tu_usuario',
            'autofocus': True,
        })
    )
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
        })
    )


class TarjetaForm(forms.Form):
    MESES = [(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)]
    anio_actual = date.today().year
    ANIOS = [(str(a), str(a)) for a in range(anio_actual, anio_actual + 11)]

    nombre_titular = forms.CharField(
        label='Nombre en la tarjeta',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Como aparece en la tarjeta',
            'autocomplete': 'cc-name',
        })
    )
    numero_tarjeta = forms.CharField(
        label='Número de tarjeta',
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '•••• •••• •••• ••••',
            'autocomplete': 'cc-number',
            'inputmode': 'numeric',
            'id': 'id_numero_tarjeta',
        })
    )
    mes_expiracion = forms.ChoiceField(
        label='Mes',
        choices=MESES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    anio_expiracion = forms.ChoiceField(
        label='Año',
        choices=ANIOS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '•••',
            'autocomplete': 'cc-csc',
            'inputmode': 'numeric',
            'maxlength': '4',
        })
    )

    def clean_numero_tarjeta(self):
        numero = self.cleaned_data['numero_tarjeta'].replace(' ', '').replace('-', '')
        if not numero.isdigit():
            raise ValidationError('El número de tarjeta solo debe contener dígitos.')
        if not (13 <= len(numero) <= 19):
            raise ValidationError('Número de tarjeta inválido.')
        return numero

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or not (3 <= len(cvv) <= 4):
            raise ValidationError('CVV inválido.')
        return cvv

    def detectar_tipo(self, numero):
        if numero.startswith('4'):
            return 'visa'
        if numero[:2] in ('51', '52', '53', '54', '55') or (2221 <= int(numero[:4]) <= 2720):
            return 'mastercard'
        if numero[:2] in ('34', '37'):
            return 'amex'
        return 'otro'
