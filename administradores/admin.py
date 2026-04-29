from django.contrib import admin
from .models import Administrador


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'email', 'activo', 'creado_en')
    list_filter = ('activo', 'creado_en')
    search_fields = ('nombre_usuario', 'email')
    readonly_fields = ('creado_en', 'actualizado_en')
    
    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('email', 'nombre_usuario', 'password')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )

