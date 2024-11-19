# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventario5.views import *
from rest_framework.views import APIView

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'detalle-compras', DetalleCompraViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')



urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include(router.urls)),
]