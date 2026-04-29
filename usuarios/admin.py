from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'email', 'nombre_completo', 'activo', 'creado_en')
    list_filter = ('activo', 'pais', 'creado_en')
    search_fields = ('nombre_usuario', 'email', 'nombre_completo', 'telefono')
    readonly_fields = ('creado_en', 'actualizado_en')

    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('email', 'nombre_usuario')
        }),
        ('Información Personal', {
            'fields': ('nombre_completo', 'telefono')
        }),
        ('Dirección de Envío', {
            'fields': ('direccion', 'ciudad', 'estado_provincia', 'codigo_postal', 'pais')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )

