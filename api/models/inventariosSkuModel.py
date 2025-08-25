from django.db import models

CLASIFICACION_CHOICES = [
    ('consignacion', 'Consignación'),
    ('controlado', 'Controlado'),
    ('normal', 'Normal'),
    ('amor', 'Amor'),
]
class InventarioSKU(models.Model):
    estado = models.CharField(max_length=12, choices=[('alta', 'Alta'), ('baja', 'Baja')], default='alta')
    categoria = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100)
    principio_activo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    codigo_sku = models.CharField(max_length=100, unique=True)
    #descripcion_estado_cuenta = models.TextField(blank=True, null=True)
    unidad_compra = models.CharField(max_length=50)
    unidad_despacho = models.CharField(max_length=50)
    unidades_por_paquete = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    clasificacion_producto = models.CharField(max_length=20, choices=CLASIFICACION_CHOICES, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    iva = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)

class BodegaSKU(models.Model):
    sku = models.ForeignKey(InventarioSKU, on_delete=models.CASCADE, related_name='bodegas')
    nombre_bodega = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    
class MovimientoBodega(models.Model):
    sku = models.ForeignKey(InventarioSKU, on_delete=models.CASCADE)
    bodega_origen = models.CharField(max_length=100)
    bodega_destino = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
