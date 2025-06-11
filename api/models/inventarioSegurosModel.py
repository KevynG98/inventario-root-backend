from django.db import models

class Seguros(models.Model):
    nombre = models.TextField()
    nit = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    contacto_nombre = models.CharField(max_length=100, blank=True, null=True)
    contacto_correo = models.EmailField(blank=True, null=True)
    contacto_telefono = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
