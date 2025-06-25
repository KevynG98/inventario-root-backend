from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        return self.name
    
class ClaveEspecial(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clave_especial')
    clave = models.CharField(max_length=100)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clave especial para {self.usuario.username}"