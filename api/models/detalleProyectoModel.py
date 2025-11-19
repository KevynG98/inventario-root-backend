from django.db import models

class DetalleProyectos(models.Model):
    proyectoId = models.ForeignKey('Proyectos', related_name='detalles', on_delete=models.CASCADE)
    productoId = models.ForeignKey('InventarioSKU', related_name='detalles_proyecto', on_delete=models.CASCADE)
    productoSubTotal = models.DecimalField(max_digits=12, decimal_places=2)