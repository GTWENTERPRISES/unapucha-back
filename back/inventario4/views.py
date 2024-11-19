from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (Categoria, Producto, Cliente, Proveedor, 
                    Venta, DetalleVenta, Compra, DetalleCompra)
from .serializers import (CategoriaSerializer, ProductoSerializer, 
                         ClienteSerializer, ProveedorSerializer,
                         VentaSerializer, VentaCreateSerializer,
                         CompraSerializer, CompraCreateSerializer)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'estado']
    search_fields = ['nombre', 'sku']
    ordering_fields = ['nombre', 'stock', 'precio']

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        productos = self.queryset.filter(estado='bajo_stock')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'email']

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'ruc']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['estado', 'metodo_pago']
    ordering_fields = ['fecha', 'total']

    def get_serializer_class(self):
        if self.action == 'create':
            return VentaCreateSerializer
        return VentaSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['estado', 'proveedor']
    ordering_fields = ['fecha', 'total']

    def get_serializer_class(self):
        if self.action == 'create':
            return CompraCreateSerializer
        return CompraSerializer