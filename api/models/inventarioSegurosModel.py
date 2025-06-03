from django.db import models

class Seguros(models.Model):
    nombre = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre