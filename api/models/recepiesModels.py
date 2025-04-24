from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombre = models.CharField(max_length=255)
    dni = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.nombre

class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="recetas")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recetas_creadas")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    procesada = models.BooleanField(default=False)

    def __str__(self):
        return f"Receta {self.id} - {self.paciente.nombre}"

class RecetaDetalle(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="detalles")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} de {self.medicamento.nombre} en {self.receta}"
