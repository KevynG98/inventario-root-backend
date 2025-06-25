from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Datos personales
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    estado_civil = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    dpi = models.CharField(max_length=20, blank=True)
    nit = models.CharField(max_length=20, blank=True)

    # Datos laborales
    departamento_laboral = models.CharField(max_length=100, blank=True)
    puesto = models.CharField(max_length=100, blank=True)
    perfil_acceso = models.CharField(max_length=100, blank=True)

    # Datos médicos (condicional)
    es_medico = models.BooleanField(default=False)
    colegiado = models.CharField(max_length=50, blank=True)
    vencimiento_colegiado = models.DateField(null=True, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)

    # Datos bancarios
    banco = models.CharField(max_length=100, blank=True)
    tipo_cuenta = models.CharField(max_length=50, blank=True)
    numero_cuenta = models.CharField(max_length=50, blank=True)
    forma_pago = models.CharField(max_length=100, blank=True)
    regimen_sat = models.CharField(max_length=100, blank=True)

    # Soft delete y fecha de alta
    estado = models.BooleanField(default=True)  # True = activo
    fecha_alta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
