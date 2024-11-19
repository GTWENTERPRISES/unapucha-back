from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Proveedor, Venta, DetalleVenta, Compra, DetalleCompra

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

from rest_framework import serializers
from .models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 
            'nombre', 
            'sku', 
            'precio', 
            'stock', 
            'stock_minimo', 
            'categoria', 
            'categoria_nombre',
            'estado', 
            'creado_en'
        ]

    def get_categoria_nombre(self, obj):
        return obj.categoria.nombre if obj.categoria else None

    def create(self, validated_data):
        categoria_id = validated_data.pop('categoria')
        categoria = Categoria.objects.get(id=categoria_id)
        producto = Producto.objects.create(
            categoria=categoria, 
            **validated_data
        )
        producto.actualizar_estado()
        return producto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = DetalleVenta
        fields = ['id', 'venta', 'producto', 'producto_nombre', 'cantidad', 
                 'precio_unitario', 'subtotal']
        read_only_fields = ['subtotal']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre')
    
    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_nombre', 'total', 'subtotal', 'iva',
                 'estado', 'metodo_pago', 'fecha', 'creado_en', 'detalles']
        read_only_fields = ['total', 'subtotal', 'iva']

class VentaCreateSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    
    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago', 'detalles']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        
        return venta

class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = DetalleCompra
        fields = ['id', 'compra', 'producto', 'producto_nombre', 'cantidad', 
                 'precio_unitario', 'subtotal']
        read_only_fields = ['subtotal']

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True, read_only=True)
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre')
    
    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'proveedor_nombre', 'total', 'subtotal', 
                 'iva', 'estado', 'numero_orden', 'fecha', 'creado_en', 'detalles']
        read_only_fields = ['total', 'subtotal', 'iva']

class CompraCreateSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    
    class Meta:
        model = Compra
        fields = ['proveedor', 'numero_orden', 'detalles']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        compra = Compra.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleCompra.objects.create(compra=compra, **detalle_data)
        
        return compra