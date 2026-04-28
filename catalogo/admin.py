from django.contrib import admin
from .models import Categoria, Producto, UsuarioPOS

@admin.register(UsuarioPOS)
class UsuarioPOSAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'correo_validado', 'creado_en')
    list_filter = ('rol', 'correo_validado', 'creado_en')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('creado_en',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono_emoji', 'creado_en')
    search_fields = ('nombre',)
    list_filter = ('creado_en',)


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
