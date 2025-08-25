from django.db import models
from django.contrib.auth import get_user_model
from .requisisionesModel import Requisicion


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("BORRADOR", "BORRADOR"),
        ("EDICION", "EDICION"),
        ("ANULADA", "ANULADA"),
        ("GENERADA", "GENERADA"),
    ]

    CONDICIONES_PAGO_CHOICES = [
        ("CREDITO", "Crédito"),
        ("CONTADO", "Contado"),
    ]

    requisicion = models.ForeignKey(Requisicion, on_delete=models.PROTECT, related_name="ordenes_compra")
    numero = models.CharField(max_length=50, blank=True, null=True, unique=True)
    estatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default="BORRADOR")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Pago / entrega
    fecha_entrega = models.DateField(blank=True, null=True)
    condiciones_pago = models.CharField(max_length=10, choices=CONDICIONES_PAGO_CHOICES, blank=True, null=True)
    dias_credito = models.IntegerField(blank=True, null=True)

    # Snapshots de datos relevantes
    proveedor_nombre = models.CharField(max_length=200, blank=True, null=True)
    solicitante_bodega = models.CharField(max_length=200, blank=True, null=True)
    tipo_requisicion = models.CharField(max_length=20, blank=True, null=True)

    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"OC {self.numero or self.id} - {self.estatus}"


class PurchaseOrderDetail(models.Model):
    orden = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    codigo_sku = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_sin_iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"Item {self.codigo_sku} ({self.cantidad})"


class PurchaseOrderLog(models.Model):
    ACCIONES = [
        ("EDITAR", "EDITAR"),
        ("ANULAR", "ANULAR"),
        ("GENERAR", "GENERAR"),
    ]

    orden = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="bitacora")
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observaciones = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.orden_id} {self.accion} por {self.usuario_id}"

