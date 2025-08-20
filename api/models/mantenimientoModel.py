from django.db import models
from django.db.models import Q


class CentroCosto(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(is_active=True),
                name='uniq_centrocosto_nombre_activo'
            )
        ]


class Departamento(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(is_active=True),
                name='uniq_departamento_nombre_activo'
            )
        ]


class CuentaContable(models.Model):
    ESTADO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
    ]
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='alta')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(is_active=True),
                name='uniq_cuentacontable_nombre_activo'
            )
        ]
