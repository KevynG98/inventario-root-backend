from django.db import models
from django.utils import timezone


def default_historial():
    return []


class Operacion(models.Model):
    class Estatus(models.TextChoices):
        PROGRAMADO = "Programado", "Programado"
        EN_PROCESO = "En Proceso", "En Proceso"
        EN_RECUPERACION = "En Recuperación", "En Recuperación"
        FINALIZADO = "Finalizado", "Finalizado"
        CANCELADA = "Cancelada", "Cancelada"

    fecha = models.DateField()
    dia = models.CharField(max_length=20)
    hora = models.CharField(max_length=20)
    paciente = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()
    especialidad = models.CharField(max_length=100)
    procedimiento = models.TextField()
    cirujano1 = models.CharField(max_length=255)
    cirujano2 = models.CharField(max_length=255, blank=True, null=True)
    cirujano3 = models.CharField(max_length=255, blank=True, null=True)
    anestesiologo = models.CharField(max_length=255, blank=True, null=True)
    pediatra = models.CharField(max_length=255, blank=True, null=True)
    seguro = models.CharField(max_length=255)
    material = models.TextField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    estatus = models.CharField(
        max_length=20, choices=Estatus.choices, default=Estatus.PROGRAMADO
    )
    historial = models.JSONField(default=default_historial, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-fecha", "hora")
        verbose_name = "Operación"
        verbose_name_plural = "Operaciones"

    def registrar_historial(self, accion, usuario=None):
        registro = {
            "accion": accion,
            "fecha": timezone.now().isoformat(),
        }
        if usuario:
            registro["usuario"] = usuario
        historial = self.historial or []
        historial.append(registro)
        self.historial = historial
        self.save(update_fields=["historial"])

    def __str__(self):
        return f"{self.fecha} - {self.paciente} - {self.procedimiento}"
