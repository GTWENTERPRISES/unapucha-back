from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADO_CHOICES = [
        ('en_stock', 'En Stock'),
        ('bajo_stock', 'Bajo Stock'),
        ('sin_stock', 'Sin Stock'),
    ]
    
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_stock')
    creado_en = models.DateTimeField(auto_now_add=True)

    def actualizar_estado(self):
        if self.stock <= 0:
            self.estado = 'sin_stock'
        elif self.stock <= self.stock_minimo:
            self.estado = 'bajo_stock'
        else:
            self.estado = 'en_stock'
        self.save()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    ruc = models.CharField(max_length=13, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    fecha = models.DateField(auto_now_add=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        self.subtotal = sum(detalle.subtotal for detalle in self.detalles.all())
        self.iva = self.subtotal * Decimal('0.12')
        self.total = self.subtotal + self.iva
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.producto.stock -= self.cantidad
        self.producto.actualizar_estado()
        self.venta.calcular_total()

    def __str__(self):
        return f"Detalle de venta #{self.venta.id} - {self.producto.nombre}"

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    numero_orden = models.CharField(max_length=20)
    fecha = models.DateField(auto_now_add=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def calcular_total(self):
        self.subtotal = sum(detalle.subtotal for detalle in self.detalles.all())
        self.iva = self.subtotal * Decimal('0.12')
        self.total = self.subtotal + self.iva
        self.save()

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor.nombre}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.producto.stock += self.cantidad
        self.producto.actualizar_estado()
        self.compra.calcular_total()

    def __str__(self):
        return f"Detalle de compra #{self.compra.id} - {self.producto.nombre}"