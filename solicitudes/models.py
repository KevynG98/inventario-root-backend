from django.db import models


class Solicitud(models.Model):
    class Estatus(models.TextChoices):
        NUEVA = "Nueva", "Nueva"
        EN_PROCESO = "En Proceso", "En Proceso"
        PENDIENTE_RECIBIR = "Pendiente de Recibir", "Pendiente de Recibir"
        CARGADO_ESTADO = "Cargado al Estado de Cuenta", "Cargado al Estado de Cuenta"

    fecha = models.DateField(auto_now_add=True)
    admision = models.CharField(max_length=50)
    paciente = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    habitacion = models.CharField(max_length=50)
    bodega_origen = models.CharField(max_length=100)
    bodega_destino = models.CharField(max_length=100)
    estatus = models.CharField(
        max_length=50,
        choices=Estatus.choices,
        default=Estatus.NUEVA,
    )

    class Meta:
        ordering = ("-fecha", "-id")

    def __str__(self) -> str:
        return f"Solicitud {self.id} - {self.admision} - {self.estatus}"


class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.CASCADE,
        related_name="detalle",
    )
    sku = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    enviada = models.IntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.sku} ({self.cantidad})"
