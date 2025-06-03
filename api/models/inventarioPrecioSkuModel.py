from django.db import models
from .inventariosSkuModel import InventarioSKU

class PrecioSKU(models.Model):
    sku = models.ForeignKey(InventarioSKU, on_delete=models.CASCADE)
    sku_nombre = models.CharField(max_length=200)  # redundante para facilidad de lectura
    seguro_nombre = models.CharField(max_length=100)  # ahora es texto plano
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    vigente_desde = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.sku_nombre} - {self.seguro_nombre} - {self.precio}'
