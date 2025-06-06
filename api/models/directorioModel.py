from django.db import models

class Directorio(models.Model):
    nivel = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    extension = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.extension})"
