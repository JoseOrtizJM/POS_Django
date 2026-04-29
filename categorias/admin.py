from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono_emoji', 'creado_en')
    search_fields = ('nombre',)
    list_filter = ('creado_en',)

