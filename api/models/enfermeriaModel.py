from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from .admisionesModel import Admision
from ..models.salidasModel import Salida  # type: ignore
from ..models.trasladosModel import Traslado  # type: ignore

INGESTA_COLUMN_IDS = [
    "ingesta_oral",
    "ingesta_enteral",
    "ingesta_parenteral",
    *[f"ingesta_iv_{index}" for index in range(1, 13)],
    "ingesta_extra_1",
    "ingesta_extra_2",
]

EXCRETA_COLUMN_IDS = [
    "excreta_orina",
    "excreta_deposicion",
    "excreta_vomito",
    "excreta_drenaje",
    *[f"excreta_otro_{index}" for index in range(1, 7)],
]

INGESTA_EXCRETA_COLUMN_IDS = INGESTA_COLUMN_IDS + EXCRETA_COLUMN_IDS

SHIFT_DEFINITIONS = (
    ("turno1", "Turno #1 (07:00 - 13:00)"),
    ("turno2", "Turno #2 (13:00 - 19:00)"),
    ("turno3", "Turno #3 (19:00 - 07:00)"),
)

SLOT_DEFINITIONS = (
    *[(f"{str(hour).zfill(2)}:00", "turno1") for hour in range(7, 13)],
    *[(f"{str(hour).zfill(2)}:00", "turno2") for hour in range(13, 19)],
    *[(f"{str(hour).zfill(2)}:00", "turno3") for hour in range(19, 24)],
    ("00:00", "turno3"),
    ("01:00", "turno3"),
    ("02:00", "turno3"),
    ("03:00", "turno3"),
    ("04:00", "turno3"),
    ("05:00", "turno3"),
    ("06:00", "turno3"),
)


def default_row_values():
    return {column: None for column in INGESTA_EXCRETA_COLUMN_IDS}


class AdmisionMedicoTratante(models.Model):
    ESTADO_CHOICES = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="medicos_tratantes"
    )
    nombre = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="ACTIVO"
    )
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Médico tratante"
        verbose_name_plural = "Médicos tratantes"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"{self.nombre} ({self.especialidad or 'Sin especialidad'})"


class HistoriaEnfermedad(models.Model):
    EDITOR_TEMAS = (
        ("SNOW", "Snow"),
        ("BUBBLE", "Bubble"),
    )

    EDITOR_TOOLBARS = (
        ("COMPLETA", "Completa"),
        ("BASICA", "Básica"),
        ("MINIMA", "Mínima"),
    )

    admision = models.OneToOneField(
        Admision,
        on_delete=models.CASCADE,
        related_name="historia_enfermedad"
    )
    contenido = models.TextField(blank=True, null=True)
    editor_tema = models.CharField(
        max_length=10,
        choices=EDITOR_TEMAS,
        default="SNOW"
    )
    editor_toolbar = models.CharField(
        max_length=10,
        choices=EDITOR_TOOLBARS,
        default="COMPLETA"
    )
    editor_placeholder = models.CharField(max_length=255, blank=True, null=True)
    editor_autoguardado = models.BooleanField(default=True)
    editor_solo_lectura = models.BooleanField(default=False)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Historia de la enfermedad"
        verbose_name_plural = "Historias de la enfermedad"

    def __str__(self):
        return f"Historia - Admisión {self.admision_id}"


class SignoVitalEmergencia(models.Model):
    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="signos_vitales_emergencia"
    )
    tomado_en = models.DateTimeField(default=timezone.now)
    registrado_por = models.CharField(max_length=150, blank=True, null=True)
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    estatura_cm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    presion_arterial = models.CharField(max_length=20, blank=True, null=True)
    presion_arterial_media = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temperatura_c = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    frecuencia_cardiaca = models.PositiveSmallIntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.PositiveSmallIntegerField(blank=True, null=True)
    oxigenacion = models.PositiveSmallIntegerField(blank=True, null=True)
    glucosa_mg_dl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    insulina_u = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    datos_extra = models.JSONField(default=dict, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Signo vital - Emergencia"
        verbose_name_plural = "Signos vitales - Emergencia"
        ordering = ("-tomado_en",)

    def __str__(self):
        return f"Signos vitales emergencia {self.admision_id} - {self.tomado_en:%Y-%m-%d %H:%M}"


class OrdenMedica(models.Model):
    ESTADOS = (
        ("ACTIVA", "Activa"),
        ("EN_PROCESO", "En proceso"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    )

    PRIORIDADES = (
        ("BAJA", "Baja"),
        ("MEDIA", "Media"),
        ("ALTA", "Alta"),
        ("URGENTE", "Urgente"),
    )

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="ordenes_medicas"
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVA")
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default="MEDIA")
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    cerrado_en = models.DateTimeField(blank=True, null=True)
    cerrado_por = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Orden médica"
        verbose_name_plural = "Órdenes médicas"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"Orden médica {self.titulo} ({self.estado})"


class OrdenMedicaEvento(models.Model):
    orden = models.ForeignKey(
        OrdenMedica,
        on_delete=models.CASCADE,
        related_name="eventos"
    )
    estado = models.CharField(max_length=20, choices=OrdenMedica.ESTADOS)
    comentario = models.TextField(blank=True, null=True)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evento de orden médica"
        verbose_name_plural = "Eventos de órdenes médicas"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"{self.orden.titulo} -> {self.estado}"


class AntecedenteClinico(models.Model):
    TIPOS = (
        ("PERSONALES", "Personales"),
        ("FAMILIARES", "Familiares"),
        ("QUIRURGICOS", "Quirúrgicos"),
        ("FARMACOLOGICOS", "Farmacológicos"),
        ("ALERGIAS", "Alergias"),
        ("OTROS", "Otros"),
    )

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="antecedentes_clinicos"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default="OTROS")
    descripcion = models.TextField()
    es_activo = models.BooleanField(default=True)
    registrado_por = models.CharField(max_length=150, blank=True, null=True)
    registrado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Antecedente clínico"
        verbose_name_plural = "Antecedentes clínicos"
        ordering = ("-registrado_en",)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.admision_id}"


class ControlMedicamento(models.Model):
    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="controles_medicamentos"
    )
    medicamento = models.CharField(max_length=200)
    dosis = models.CharField(max_length=100, blank=True, null=True)
    via = models.CharField(max_length=50, blank=True, null=True)
    frecuencia = models.CharField(max_length=50, blank=True, null=True)
    indicaciones = models.TextField(blank=True, null=True)
    inicio_programado = models.DateTimeField(blank=True, null=True)
    fin_programado = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Control de medicamento"
        verbose_name_plural = "Controles de medicamentos"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"{self.medicamento} ({self.admision_id})"


class ControlMedicamentoRegistro(models.Model):
    ESTADOS = (
        ("PENDIENTE", "Pendiente"),
        ("APLICADO", "Aplicado"),
        ("OMITIDO", "Omitido"),
        ("CAMBIO", "Cambio"),
    )

    control = models.ForeignKey(
        ControlMedicamento,
        on_delete=models.CASCADE,
        related_name="registros"
    )
    bloque = models.CharField(max_length=32)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="PENDIENTE")
    comentario = models.TextField(blank=True, null=True)
    registrado_por = models.CharField(max_length=150, blank=True, null=True)
    registrado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de medicamento"
        verbose_name_plural = "Registros de medicamentos"
        ordering = ("-registrado_en",)

    def __str__(self):
        return f"{self.control.medicamento} - {self.bloque}"


class NotaEnfermeria(models.Model):
    ESTADOS = (
        ("EDICION", "En edición"),
        ("CERRADA", "Cerrada"),
    )

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="notas_enfermeria"
    )
    turno = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="EDICION")
    contenido = models.TextField(blank=True, null=True)
    autor = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    cerrado_en = models.DateTimeField(blank=True, null=True)
    cerrado_por = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Nota de enfermería"
        verbose_name_plural = "Notas de enfermería"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"Nota {self.turno} ({self.estado})"


class EvolucionClinica(models.Model):
    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="evoluciones_clinicas"
    )
    resumen = models.CharField(max_length=255, blank=True, null=True)
    contenido = models.TextField()
    medico_nombre = models.CharField(max_length=255, blank=True, null=True)
    medico_colegiado = models.CharField(max_length=100, blank=True, null=True)
    creado_por_username = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por_username = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evolución clínica"
        verbose_name_plural = "Evoluciones clínicas"
        ordering = ("-creado_en",)

    def __str__(self):
        return f"Evolución {self.admision_id} - {self.creado_en:%Y-%m-%d %H:%M}"


class RegistroDieta(models.Model):
    TIEMPOS = (
        ("DESAYUNO", "Desayuno"),
        ("ALMUERZO", "Almuerzo"),
        ("CENA", "Cena"),
        ("MERIENDA", "Merienda"),
        ("SNACK", "Snack"),
        ("OTRO", "Otro"),
    )

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="registros_dieta"
    )
    tiempo = models.CharField(max_length=20, choices=TIEMPOS, default="OTRO")
    dieta = models.CharField(max_length=150)
    observaciones = models.TextField(blank=True, null=True)
    registrado_por = models.CharField(max_length=150, blank=True, null=True)
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de dieta"
        verbose_name_plural = "Registros de dietas"
        ordering = ("-registrado_en",)

    def __str__(self):
        return f"{self.dieta} - {self.admision_id}"


class SignoVitalEncamamiento(models.Model):
    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="signos_vitales_encamamiento"
    )
    tomado_en = models.DateTimeField(default=timezone.now)
    registrado_por = models.CharField(max_length=150, blank=True, null=True)
    mediciones = models.JSONField(default=dict, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Signo vital - Encamamiento"
        verbose_name_plural = "Signos vitales - Encamamiento"
        ordering = ("-tomado_en",)

    def __str__(self):
        return f"Signos encamamiento {self.admision_id} - {self.tomado_en:%Y-%m-%d %H:%M}"


class IngestaExcretaDia(models.Model):
    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="ingestas_excretas"
    )
    fecha = models.DateField()
    columnas_personalizadas = models.JSONField(default=dict, blank=True)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro diario de ingesta/excreta"
        verbose_name_plural = "Registros diarios de ingesta/excreta"
        ordering = ("-fecha", "-creado_en")
        unique_together = ("admision", "fecha")

    def __str__(self):
        return f"Ingesta/Excreta {self.admision_id} - {self.fecha}"

    def ensure_registros(self):
        existentes = set(self.registros.values_list("slot", flat=True))
        faltantes = [
            (slot, turno) for slot, turno in SLOT_DEFINITIONS if slot not in existentes
        ]
        registros = [
            IngestaExcretaRegistro(
                dia=self,
                slot=slot,
                turno=turno,
                valores=default_row_values()
            )
            for slot, turno in faltantes
        ]
        if registros:
            IngestaExcretaRegistro.objects.bulk_create(registros)


class IngestaExcretaRegistro(models.Model):
    slot_validator = RegexValidator(
        regex=r"^\d{2}:\d{2}$",
        message="El formato de la hora debe ser HH:MM."
    )

    dia = models.ForeignKey(
        IngestaExcretaDia,
        on_delete=models.CASCADE,
        related_name="registros"
    )
    slot = models.CharField(max_length=5, validators=[slot_validator])
    turno = models.CharField(max_length=10, choices=SHIFT_DEFINITIONS)
    valores = models.JSONField(default=default_row_values, blank=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de ingesta/excreta por hora"
        verbose_name_plural = "Registros de ingesta/excreta por hora"
        ordering = ("slot",)
        unique_together = ("dia", "slot")

    def __str__(self):
        return f"{self.slot} - {self.dia_id}"


class SolicitudMedicamento(models.Model):
    class Estados(models.TextChoices):
        PENDIENTE_ENVIAR = "PENDIENTE_ENVIAR", "Pendiente de Enviar"
        ENVIADA = "ENVIADA", "Enviada"
        PENDIENTE_RECIBIR = "PENDIENTE_RECIBIR", "Pendiente de Recibir"
        RECIBIDA = "RECIBIDA", "Recibida - Pendiente de Cargar a EC"
        CARGADA_EC = "CARGADA_EC", "Cargada al Estado de Cuenta"
        ANULADA = "ANULADA", "Anulada"

    admision = models.ForeignKey(
        Admision,
        on_delete=models.CASCADE,
        related_name="solicitudes_medicamentos"
    )
    bodega_origen = models.CharField(max_length=120)
    bodega_destino = models.CharField(max_length=120)
    comentarios = models.TextField(blank=True, null=True)
    estatus = models.CharField(
        max_length=40,
        choices=Estados.choices,
        default=Estados.PENDIENTE_ENVIAR
    )
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True)
    enviado_por = models.CharField(max_length=150, blank=True, null=True)
    recibido_por = models.CharField(max_length=150, blank=True, null=True)
    cargado_por = models.CharField(max_length=150, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_recibido = models.DateTimeField(blank=True, null=True)
    fecha_cargado_ec = models.DateTimeField(blank=True, null=True)

    traslado_recibo = models.ForeignKey(
        Traslado,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="solicitudes_medicamento"
    )
    salida_cuenta = models.ForeignKey(
        Salida,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="solicitudes_medicamento"
    )

    def __str__(self):
        return f"SolicitudMedicamento #{self.pk} ({self.estatus})"


class SolicitudMedicamentoItem(models.Model):
    solicitud = models.ForeignKey(
        SolicitudMedicamento,
        on_delete=models.CASCADE,
        related_name="items"
    )
    orden_medica_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=120, blank=True, null=True)
    subcategoria = models.CharField(max_length=120, blank=True, null=True)
    cantidad_pedida = models.PositiveIntegerField(default=0)
    cantidad_enviada = models.PositiveIntegerField(default=0)
    cantidad_recibida = models.PositiveIntegerField(default=0)
    cantidad_devuelta = models.PositiveIntegerField(default=0)
    comentario_far = models.TextField(blank=True, null=True)
    comentario_enfermeria = models.TextField(blank=True, null=True)
    recibido = models.BooleanField(default=False)
    devuelto = models.BooleanField(default=False)
    traslado_devolucion = models.ForeignKey(
        Traslado,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="items_devueltos"
    )
    devuelto_en = models.DateTimeField(blank=True, null=True)
    devuelto_por = models.CharField(max_length=150, blank=True, null=True)
    usuario_traslado_devolucion = models.CharField(max_length=150, blank=True, null=True)
    departamento_traslado_devolucion = models.CharField(max_length=150, blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ítem de solicitud de medicamentos"
        verbose_name_plural = "Ítems de solicitud de medicamentos"
        ordering = ("id",)

    def __str__(self):
        return f"{self.sku} ({self.cantidad_pedida})"
