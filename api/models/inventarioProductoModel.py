from django.db import models

class InventarioProducto(models.Model):
    estado = models.CharField(max_length=12, choices=[('alta', 'Alta'), ('baja', 'Baja')], default='alta')
    categoria = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100)
    principio_activo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    codigo_inventario = models.CharField(max_length=100, unique=True)
    unidad_compra = models.CharField(max_length=50)
    unidad_despacho = models.CharField(max_length=50)
    unidades_por_paquete = models.PositiveIntegerField(default=1)
    precio_compre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
