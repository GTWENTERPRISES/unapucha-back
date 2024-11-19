from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Producto)
admin.site.register(Proveedor)
