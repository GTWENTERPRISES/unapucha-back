# Generated by Django 5.1.1 on 2024-11-19 12:21

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario4', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('direccion', models.TextField(blank=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoría', 'verbose_name_plural': 'Categorías'},
        ),
        migrations.AlterModelOptions(
            name='compra',
            options={'verbose_name': 'Compra', 'verbose_name_plural': 'Compras'},
        ),
        migrations.AlterModelOptions(
            name='detallecompra',
            options={},
        ),
        migrations.AlterModelOptions(
            name='detalleventa',
            options={},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterModelOptions(
            name='venta',
            options={'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
        migrations.RemoveConstraint(
            model_name='detallecompra',
            name='check_cantidad_compra_positiva',
        ),
        migrations.RemoveConstraint(
            model_name='detalleventa',
            name='check_cantidad_positiva',
        ),
        migrations.RemoveConstraint(
            model_name='detalleventa',
            name='check_descuento_rango',
        ),
        migrations.RemoveConstraint(
            model_name='producto',
            name='check_stock_minimo_menor_maximo',
        ),
        migrations.RemoveIndex(
            model_name='categoria',
            name='inventario4_nombre_39b633_idx',
        ),
        migrations.RemoveIndex(
            model_name='categoria',
            name='inventario4_slug_81dad3_idx',
        ),
        migrations.RemoveIndex(
            model_name='compra',
            name='inventario4_numero__d91e87_idx',
        ),
        migrations.RemoveIndex(
            model_name='compra',
            name='inventario4_fecha_f719f9_idx',
        ),
        migrations.RemoveIndex(
            model_name='compra',
            name='inventario4_estado_92c72d_idx',
        ),
        migrations.RemoveIndex(
            model_name='compra',
            name='inventario4_proveed_bd5492_idx',
        ),
        migrations.RemoveIndex(
            model_name='detallecompra',
            name='inventario4_compra__9fe2cc_idx',
        ),
        migrations.RemoveIndex(
            model_name='detallecompra',
            name='inventario4_product_d833e0_idx',
        ),
        migrations.RemoveIndex(
            model_name='detalleventa',
            name='inventario4_venta_i_ce9d38_idx',
        ),
        migrations.RemoveIndex(
            model_name='detalleventa',
            name='inventario4_product_04bed7_idx',
        ),
        migrations.RemoveIndex(
            model_name='producto',
            name='inventario4_nombre_06af1f_idx',
        ),
        migrations.RemoveIndex(
            model_name='producto',
            name='inventario4_sku_00b9df_idx',
        ),
        migrations.RemoveIndex(
            model_name='producto',
            name='inventario4_estado__f1ddf4_idx',
        ),
        migrations.RemoveIndex(
            model_name='producto',
            name='inventario4_categor_b0aa3c_idx',
        ),
        migrations.RemoveIndex(
            model_name='proveedor',
            name='inventario4_nombre_5aa85d_idx',
        ),
        migrations.RemoveIndex(
            model_name='proveedor',
            name='inventario4_ruc_e98843_idx',
        ),
        migrations.RemoveIndex(
            model_name='proveedor',
            name='inventario4_email_f9c5d7_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_numero__9ba0f6_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_fecha_8fe48e_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_estado_92409b_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_cliente_29eeb9_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_cedula__57d161_idx',
        ),
        migrations.RemoveIndex(
            model_name='venta',
            name='inventario4_metodo__3ead06_idx',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='activa',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='numero_factura',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='total_base',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='total_con_iva',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='total_iva',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='detallecompra',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='detallecompra',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='descuento',
        ),
        migrations.RemoveField(
            model_name='detalleventa',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='estado_stock',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='precio_base',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='stock_maximo',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='contacto',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='provincia',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='cedula_ruc',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='email',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='numero_factura',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='total_base',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='total_con_iva',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='total_iva',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='compra',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compra',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='compra',
            name='numero_orden',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compra',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='compra',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='producto',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('en_stock', 'En Stock'), ('bajo_stock', 'Bajo Stock'), ('sin_stock', 'Sin Stock')], default='en_stock', max_length=20),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proveedor',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='venta',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='venta',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoria',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('recibido', 'Recibido'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='compra',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario4.proveedor'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='inventario4.compra'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario4.producto'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario4.producto'),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='inventario4.venta'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario4.categoria'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='sku',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_minimo',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='direccion',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='ruc',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='venta',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('completado', 'Completado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia')], max_length=20),
        ),
        migrations.AlterField(
            model_name='venta',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario4.cliente'),
        ),
    ]