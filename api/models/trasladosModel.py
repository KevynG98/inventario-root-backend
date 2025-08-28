from django.db import models


class Traslado(models.Model):
    ESTATUS_CHOICES = [
        ('ENVIADO', 'Enviado'),
        ('RECIBIDO', 'Recibido'),
        ('ANULADO', 'Anulado'),
    ]

    bodega_origen = models.CharField(max_length=100)
    bodega_destino = models.CharField(max_length=100)
    comentarios = models.TextField(blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)

    enviado_por = models.CharField(max_length=150, blank=True, null=True)
    entregamos_a = models.CharField(max_length=150, blank=True, null=True)
    recibido_por = models.CharField(max_length=150, blank=True, null=True)

    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='ENVIADO')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_recibido = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Traslado #{self.id} ({self.estatus})"


class TrasladoItem(models.Model):
    traslado = models.ForeignKey(Traslado, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.PositiveIntegerField()
