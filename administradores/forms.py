from django import forms


class LoginAdminForm(forms.Form):
    identificador = forms.CharField(
        label='Correo o Nombre de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@correo.com  o  admin_usuario',
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
