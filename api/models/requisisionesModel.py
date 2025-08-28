from django.db import models

class Requisicion(models.Model):
    PRIORIDAD_CHOICES = [
        ('urgente', 'Urgente'),
        ('alta', 'Alta'),
        ('normal', 'Normal'),
        ('baja', 'Baja'),
    ]

    TIPO_CHOICES = [
        ('bien', 'Bien'),
        ('servicio', 'Servicio'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada',  'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cerrada',   'Cerrada'),
    ]

    bodega           = models.CharField(max_length=80)
    usuario          = models.CharField(max_length=150, null=True, blank=True)
    proveedor        = models.CharField(max_length=150, null=True, blank=True)
    estado_actualizado_por = models.CharField(max_length=150, null=True, blank=True)
    prioridad        = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    descripcion      = models.TextField(blank=True)
    centro_costo     = models.CharField(max_length=80)
    area_solicitante = models.CharField(max_length=80)
    tipo_requisicion = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado           = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Requisición #{self.id} ({self.estado})'

class ProductoRequisicion(models.Model):
    requisicion = models.ForeignKey(Requisicion, related_name='productos', on_delete=models.CASCADE)
    sku         = models.CharField(max_length=100)
    descripcion = models.TextField()
    unidad      = models.CharField(max_length=30)
    cantidad    = models.DecimalField(max_digits=10, decimal_places=2)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    total       = models.DecimalField(max_digits=10, decimal_places=2)

class ServicioRequisicion(models.Model):
    requisicion = models.ForeignKey(Requisicion, related_name='servicios', on_delete=models.CASCADE)
    descripcion = models.TextField()
    cantidad    = models.DecimalField(max_digits=10, decimal_places=2)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    total       = models.DecimalField(max_digits=10, decimal_places=2)
