from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (Categoria, Producto, Cliente, Proveedor, 
                    Venta, DetalleVenta, Compra, DetalleCompra)
from .serializers import (CategoriaSerializer, ProductoSerializer, 
                         ClienteSerializer, ProveedorSerializer,
                         VentaSerializer, VentaCreateSerializer,
                         DetalleVentaSerializer, CompraSerializer, 
                         CompraCreateSerializer, DetalleCompraSerializer)
from rest_framework.permissions import AllowAny
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes=[AllowAny]
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        productos = self.queryset.filter(estado__in=['bajo_stock', 'sin_stock'])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Ensure categoria is an integer ID
        if isinstance(request.data.get('categoria'), dict):
            request.data['categoria'] = request.data['categoria'].get('id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        productos = self.queryset.filter(estado='bajo_stock')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes=[AllowAny]
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes=[AllowAny]
from rest_framework import viewsets
from .models import Venta
from .serializers import VentaSerializer, VentaCreateSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return VentaCreateSerializer
        return VentaSerializer

    def perform_create(self, serializer):
        detalles_data = self.request.data.get('detalles', [])
        venta = serializer.save()

        # Crear detalles de venta asociados
        for detalle in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            detalles_data = request.data.get('detalles', [])
            venta = serializer.save()

            # Actualizar o crear detalles de venta
            for detalle in detalles_data:
                detalle_id = detalle.get('id')
                if detalle_id:
                    detalle_obj = DetalleVenta.objects.get(id=detalle_id)
                    detalle_obj.cantidad = detalle['cantidad']
                    detalle_obj.precio_unitario = detalle['precio_unitario']
                    detalle_obj.save()
                else:
                    DetalleVenta.objects.create(venta=venta, **detalle)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import viewsets
from .models import DetalleVenta
from .serializers import DetalleVentaSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

    

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    permission_classes=[AllowAny]
    def get_serializer_class(self):
        if self.action == 'create':
            return CompraCreateSerializer
        return CompraSerializer

class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes=[AllowAny]







from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Venta, Cliente

@api_view(['PUT'])
def editar_venta(request, pk):
    try:
        venta = Venta.objects.get(pk=pk)
    except Venta.DoesNotExist:
        return Response({"error": "Venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    try:
        cliente = Cliente.objects.get(nombre=data.get('cliente'))
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

    venta.cliente = cliente
    venta.estado = data.get('estado')
    venta.metodo_pago = data.get('metodo_pago')
    venta.calcular_total()  # Recalcula subtotal, IVA y total automáticamente
    venta.save()

    return Response({"mensaje": "Venta actualizada correctamente"}, status=status.HTTP_200_OK)





from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Venta, DetalleVenta

def sale_details_view(request, sale_id):
    sale = get_object_or_404(Venta, id=sale_id)
    if request.method == 'GET':
        detalles = sale.detalles.all()  # Get all sale details
        return JsonResponse({'detalles': list(detalles.values())})

    if request.method == 'PUT':
        # Handle the update logic here
        # You can extract the details from request.body and update the sale details
        pass



# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from datetime import timedelta

from .models import Venta, Compra, Producto

class DashboardViewSet(viewsets.ViewSet):
    def list(self, request):
        # Lógica del dashboard principal
        un_mes_atras = timezone.now() - timedelta(days=30)

        try:
            # Ventas totales del último mes
            ventas_totales = Venta.objects.filter(
                fecha__gte=un_mes_atras
            ).aggregate(
                total=Sum('total')
            )['total'] or 0

            # Compras totales del último mes
            compras_totales = Compra.objects.filter(
                fecha__gte=un_mes_atras
            ).aggregate(
                total=Sum('total')
            )['total'] or 0

            # Total de productos en inventario
            total_productos = Producto.objects.count()

            # Productos con bajo stock
            productos_bajo_stock = Producto.objects.filter(
                stock__lte=F('stock_minimo')
            ).count()

            # Cálculo de ganancias
            ganancias = ventas_totales - compras_totales

            return Response({
                'ventas_totales': round(ventas_totales, 2),
                'compras_totales': round(compras_totales, 2),
                'total_productos': total_productos,
                'productos_bajo_stock': productos_bajo_stock,
                'ganancias': round(ganancias, 2)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def estadisticas_mensuales(self, request):
        un_anio_atras = timezone.now() - timedelta(days=365)
        
        # Ventas mensuales
        ventas_mensuales = Venta.objects.filter(
            fecha__gte=un_anio_atras
        ).annotate(
            mes=TruncMonth('fecha')
        ).values('mes').annotate(
            total_ventas=Sum('total')
        ).order_by('mes')

        # Compras mensuales
        compras_mensuales = Compra.objects.filter(
            fecha__gte=un_anio_atras
        ).annotate(
            mes=TruncMonth('fecha')
        ).values('mes').annotate(
            total_compras=Sum('total')
        ).order_by('mes')

        return Response({
            'ventas_mensuales': list(ventas_mensuales),
            'compras_mensuales': list(compras_mensuales)
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def resumen_clientes(self, request):
        # Top clientes por compras
        top_clientes = Venta.objects.values(
            'cliente__nombre', 
            'cliente__apellido'
        ).annotate(
            total_compras=Sum('total')
        ).order_by('-total_compras')[:10]

        return Response({
            'top_clientes': list(top_clientes)
        }, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def transacciones_recientes(self, request):
        try:
            # Log de inicio
            logger.info("Iniciando carga de transacciones recientes")

            # Obtener ventas con detalles y cliente
            ventas = Venta.objects.prefetch_related(
                Prefetch('detalles', 
                        queryset=DetalleVenta.objects.select_related('producto'))
            ).select_related('cliente').order_by('-creado_en')[:5]

            # Obtener compras con detalles y proveedor
            compras = Compra.objects.prefetch_related(
                Prefetch('detalles', 
                        queryset=DetalleCompra.objects.select_related('producto'))
            ).select_related('proveedor').order_by('-creado_en')[:5]

            # Log de consultas
            logger.info(f"Ventas encontradas: {ventas.count()}")
            logger.info(f"Compras encontradas: {compras.count()}")

            datos_transacciones = []

            # Procesar ventas
            for venta in ventas:
                try:
                    # Intenta obtener el primer detalle de venta
                    primer_detalle = venta.detalles.first()
                    
                    # Log de detalle de venta
                    logger.info(f"Detalle de venta: {primer_detalle}")

                    datos_transacciones.append({
                        'id': venta.id,
                        'tipo': 'Venta',
                        'cliente': venta.cliente.nombre,
                        'producto': primer_detalle.producto.nombre if primer_detalle and primer_detalle.producto else 'Sin producto',
                        'monto': float(venta.total),
                        'fecha': venta.creado_en.isoformat(),
                        'estado': venta.estado
                    })
                except Exception as detail_error:
                    logger.error(f"Error procesando detalle de venta: {detail_error}")

            # Procesar compras
            for compra in compras:
                try:
                    # Intenta obtener el primer detalle de compra
                    primer_detalle = compra.detalles.first()
                    
                    # Log de detalle de compra
                    logger.info(f"Detalle de compra: {primer_detalle}")

                    datos_transacciones.append({
                        'id': compra.id,
                        'tipo': 'Compra',
                        'proveedor': compra.proveedor.nombre,
                        'producto': primer_detalle.producto.nombre if primer_detalle and primer_detalle.producto else 'Sin producto',
                        'monto': float(compra.total),
                        'fecha': compra.creado_en.isoformat(),
                        'estado': compra.estado
                    })
                except Exception as detail_error:
                    logger.error(f"Error procesando detalle de compra: {detail_error}")

            # Ordenar y limitar transacciones
            datos_transacciones.sort(key=lambda x: x['fecha'], reverse=True)
            datos_transacciones = datos_transacciones[:5]

            # Log de transacciones finales
            logger.info(f"Transacciones finales: {len(datos_transacciones)}")

            return Response({
                'transacciones': datos_transacciones
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Log de error general
            logger.error(f"Error en transacciones recientes: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


