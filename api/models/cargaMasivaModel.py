from django.db import models


class CargaMasivaExistencia(models.Model):
    bodega = models.CharField(max_length=150)
    usuario = models.CharField(max_length=150, blank=True, null=True)
    archivo_nombre = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CargaMasivaExistenciaItem(models.Model):
    carga = models.ForeignKey(CargaMasivaExistencia, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    cantidad_cargada = models.IntegerField()
    cantidad_anterior = models.IntegerField(default=0)
    cantidad_resultante = models.IntegerField(default=0)


class CargaMasivaPrecio(models.Model):
    seguro = models.CharField(max_length=150)
    usuario = models.CharField(max_length=150, blank=True, null=True)
    archivo_nombre = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CargaMasivaPrecioItem(models.Model):
    carga = models.ForeignKey(CargaMasivaPrecio, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio_anterior = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_nuevo = models.DecimalField(max_digits=12, decimal_places=2)
