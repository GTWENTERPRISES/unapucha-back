from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Proveedor, Venta, DetalleVenta, Compra, DetalleCompra

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True)
    categoria_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'sku', 'precio', 'stock', 'stock_minimo', 'categoria', 'categoria_nombre', 'estado', 'creado_en']

    def get_categoria_nombre(self, obj):
        return obj.categoria.nombre if obj.categoria else None

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

from rest_framework import serializers
from .models import DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']



class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'cliente_nombre', 'total', 'estado', 'metodo_pago']

    def validate_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("El total debe ser un valor positivo.")
        return value

class VentaCreateSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago', 'detalles']
    
    def create(self, validated_data):
        detalles = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        for detalle in detalles:
            DetalleVenta.objects.create(venta=venta, **detalle)
        venta.calcular_total()
        return venta


class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = DetalleCompra
        fields = ['id', 'compra', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['subtotal']

class CompraSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)

    class Meta:
        model = Compra
        fields = ['id', 'fecha', 'proveedor_nombre', 'total', 'estado', 'numero_orden']

class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['proveedor', 'numero_orden', 'detalles']
    
    def create(self, validated_data):
        detalles = validated_data.pop('detalles')
        compra = Compra.objects.create(**validated_data)
        for detalle in detalles:
            DetalleCompra.objects.create(compra=compra, **detalle)
        compra.calcular_total()
        return compra