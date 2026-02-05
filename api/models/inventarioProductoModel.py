from django.db import models

class InventarioProducto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_inventario = models.CharField(max_length=100, unique=True)
    precio_compre = models.DecimalField(max_digits=12, decimal_places=2, default=0) # Coste
    precio_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Precio de venta
    is_active = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)