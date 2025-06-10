from django.db import models
from .inventariosSkuModel import InventarioSKU

class MovimientoHistorico(models.Model):
    sku = models.ForeignKey(InventarioSKU, on_delete=models.CASCADE)
    fecha = models.DateField()

    inventario_inicial = models.IntegerField()

    orden_compra = models.IntegerField(default=0)
    requisicion = models.IntegerField(default=0)
    solicitud_med = models.IntegerField(default=0)
    devolucion = models.IntegerField(default=0)
    traslado = models.IntegerField(default=0)
    salida = models.IntegerField(default=0)

    inventario_final = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} - {self.sku.codigo_sku}"
