from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UsuarioPOS, validar_email
import re


class RegistroForm(forms.Form):
    """Formulario para registrar un nuevo usuario"""
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
            'required': True
        })
    )
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa una contraseña segura',
            'required': True
        }),
        min_length=8,
        help_text='Mínimo 8 caracteres'
    )
    contrasena_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'required': True
        })
    )
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        
        # Validar formato de email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ValidationError('Por favor ingresa un correo electrónico válido')
        
        # Verificar que no exista
        if User.objects.filter(email=correo).exists():
            raise ValidationError('Este correo ya está registrado')
        
        return correo
    
    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        contrasena_confirm = cleaned_data.get('contrasena_confirm')
        
        if contrasena and contrasena_confirm:
            if contrasena != contrasena_confirm:
                raise ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data


class LoginForm(forms.Form):
    """Formulario para iniciar sesión"""
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
            'required': True
        })
    )
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'required': True
        })
    )
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        
        # Validar formato de email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ValidationError('Por favor ingresa un correo electrónico válido')
        
        return correo
