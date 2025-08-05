from django.db import models

class Principios(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]
    nombre = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre