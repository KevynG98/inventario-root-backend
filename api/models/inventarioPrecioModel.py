from django.db import models
from .inventarioProductoModel import InventarioProducto

class PrecioInventario(models.Model):
    inventario = models.ForeignKey(InventarioProducto, on_delete=models.CASCADE)
    inventario_nombre = models.CharField(max_length=200)  # redundante para facilidad de lectura
    seguro_nombre = models.CharField(max_length=100)  # ahora es texto plano
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    vigente_desde = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.inventario_nombre} - {self.seguro_nombre} - {self.precio}'
