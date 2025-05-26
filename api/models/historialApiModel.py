from django.db import models
from django.contrib.auth.models import User

class HistorialAPI(models.Model):
    metodo = models.CharField(max_length=10)
    endpoint = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cuerpo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    exito = models.BooleanField(default=True)
    codigo_respuesta = models.IntegerField()
    respuesta = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metodo} - {self.endpoint} ({'OK' if self.exito else 'ERROR'})"
