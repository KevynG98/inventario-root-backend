from django.db import models


class Entrada(models.Model):
    TIPO_CHOICES = [
        ('ajuste', 'Ajuste'),
        ('compra', 'Compra'),
        ('devolucion', 'Devolución'),
        ('inventario_inicial', 'Inventario Inicial'),
    ]
    ESTADO_CHOICES = [
        ('no_aplicada', 'No Aplicada'),
        ('aplicada', 'Aplicada'),
    ]

    bodega = models.CharField(max_length=100)
    tipo_entrada = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero_referencia = models.CharField(max_length=100, blank=True, null=True)
    orden_compra_id = models.IntegerField(blank=True, null=True)

    proveedor = models.CharField(max_length=200, blank=True, null=True)
    centro_costo = models.CharField(max_length=200, blank=True, null=True)
    cuenta_contable = models.CharField(max_length=200, blank=True, null=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='no_aplicada')
    # Usuario que creó la entrada
    usuario = models.CharField(max_length=150, blank=True, null=True)
    # Usuario que aplicó la entrada
    aplicado_por = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entrada #{self.id} ({self.estado})"


class EntradaItem(models.Model):
    entrada = models.ForeignKey(Entrada, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_sin_iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
