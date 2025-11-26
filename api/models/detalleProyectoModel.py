from django.db import models

class DetalleProyectos(models.Model):
    proyectoId = models.ForeignKey('Proyectos', related_name='detalles', on_delete=models.CASCADE)
    productoId = models.ForeignKey('InventarioProducto', related_name='detalles_proyecto', on_delete=models.CASCADE)
    cantidadProducto = models.IntegerField(default=1)
    productoSubTotal = models.DecimalField(max_digits=12, decimal_places=2)
