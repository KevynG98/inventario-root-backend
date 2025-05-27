from django.db import models

class Medida(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]
    siglas = models.TextField()
    nombre = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre