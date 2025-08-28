from django.db import models


class Salida(models.Model):
    TIPO_CHOICES = [
        ('ajuste', 'Ajuste'),
        ('devolucion', 'Devolución'),
        ('perdida', 'Pérdida'),
        ('destruccion', 'Destrucción'),
        ('venta', 'Venta'),
        ('paciente', 'Paciente'),
    ]

    bodega = models.CharField(max_length=100)
    tipo_salida = models.CharField(max_length=20, choices=TIPO_CHOICES)
    observaciones = models.TextField(blank=True, null=True)

    proveedor = models.CharField(max_length=200, blank=True, null=True)
    centro_costo = models.CharField(max_length=200, blank=True, null=True)
    cuenta_contable = models.CharField(max_length=200, blank=True, null=True)

    # Datos para tipo de salida 'paciente'
    area = models.CharField(max_length=100, blank=True, null=True)
    admision = models.IntegerField(blank=True, null=True)

    # Usuario que creó/aplicó la salida
    usuario = models.CharField(max_length=150, blank=True, null=True)
    aplicado_por = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salida #{self.id}"


class SalidaItem(models.Model):
    salida = models.ForeignKey(Salida, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_sin_iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
