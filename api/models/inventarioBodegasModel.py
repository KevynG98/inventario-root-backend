from django.db import models

class Bodegas(models.Model):
    nombre = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Cajero(models.Model):
    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=100, unique=True)
    bodega = models.ForeignKey(Bodegas, on_delete=models.CASCADE, related_name='cajeros')
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.bodega.nombre})"