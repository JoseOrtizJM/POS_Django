from django.contrib import admin
from .models import Venta, VentaItem


class VentaItemInline(admin.TabularInline):
    model = VentaItem
    extra = 0
    readonly_fields = ('nombre_producto', 'precio_unitario', 'cantidad', 'subtotal')


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'metodo_pago')
    list_filter = ('metodo_pago', 'fecha')
    readonly_fields = ('fecha',)
    inlines = [VentaItemInline]
