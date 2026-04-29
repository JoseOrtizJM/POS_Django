from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'gramaje', 'categoria', 'precio', 'stock', 'activo')
    search_fields = ('nombre', 'marca', 'categoria__nombre')
    list_filter = ('categoria', 'activo', 'creado_en')
    readonly_fields = ('creado_en', 'actualizado_en')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'marca', 'gramaje', 'categoria')
        }),
        ('Detalles de Paquete', {
            'fields': ('tipo_paquete', 'piezas_por_paquete')
        }),
        ('Precio e Inventario', {
            'fields': ('precio', 'stock')
        }),
        ('Multimedia', {
            'fields': ('imagen',)
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )

