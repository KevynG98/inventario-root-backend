from django.db import models

class Habitacion(models.Model):
    codigo = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    paciente = models.CharField(max_length=200, null=True, blank=True)
    nivel = models.CharField(max_length=50)
    observacion = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Soft delete

    def __str__(self):
        return f"{self.codigo} - {self.area}"
