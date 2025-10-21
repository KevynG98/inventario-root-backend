from rest_framework import serializers

from ..models.enfermeriaModel import (
    AdmisionMedicoTratante,
    AntecedenteClinico,
    ControlMedicamento,
    ControlMedicamentoRegistro,
    HistoriaEnfermedad,
    NotaEnfermeria,
    OrdenMedica,
    OrdenMedicaEvento,
    RegistroDieta,
    SignoVitalEmergencia,
    SignoVitalEncamamiento,
)


class AdmisionMedicoTratanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmisionMedicoTratante
        fields = [
            "id",
            "admision",
            "nombre",
            "especialidad",
            "telefono",
            "correo",
            "observaciones",
            "estado",
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class HistoriaEnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaEnfermedad
        fields = [
            "id",
            "admision",
            "contenido",
            "editor_tema",
            "editor_toolbar",
            "editor_placeholder",
            "editor_autoguardado",
            "editor_solo_lectura",
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class SignoVitalEmergenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignoVitalEmergencia
        fields = [
            "id",
            "admision",
            "tomado_en",
            "registrado_por",
            "peso_kg",
            "estatura_cm",
            "presion_arterial",
            "presion_arterial_media",
            "temperatura_c",
            "frecuencia_cardiaca",
            "frecuencia_respiratoria",
            "oxigenacion",
            "glucosa_mg_dl",
            "insulina_u",
            "comentarios",
            "datos_extra",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class SignoVitalEncamamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignoVitalEncamamiento
        fields = [
            "id",
            "admision",
            "tomado_en",
            "registrado_por",
            "mediciones",
            "comentarios",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class AntecedenteClinicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntecedenteClinico
        fields = [
            "id",
            "admision",
            "tipo",
            "descripcion",
            "es_activo",
            "registrado_por",
            "registrado_en",
            "actualizado_en",
        ]
        read_only_fields = ("registrado_en", "actualizado_en")


class ControlMedicamentoRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlMedicamentoRegistro
        fields = [
            "id",
            "control",
            "bloque",
            "estado",
            "comentario",
            "registrado_por",
            "registrado_en",
            "actualizado_en",
        ]
        read_only_fields = ("registrado_en", "actualizado_en")


class ControlMedicamentoSerializer(serializers.ModelSerializer):
    registros = ControlMedicamentoRegistroSerializer(many=True, read_only=True)

    class Meta:
        model = ControlMedicamento
        fields = [
            "id",
            "admision",
            "medicamento",
            "dosis",
            "via",
            "frecuencia",
            "indicaciones",
            "inicio_programado",
            "fin_programado",
            "activo",
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
            "registros",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class NotaEnfermeriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaEnfermeria
        fields = [
            "id",
            "admision",
            "turno",
            "estado",
            "contenido",
            "autor",
            "creado_en",
            "actualizado_en",
            "cerrado_en",
            "cerrado_por",
        ]
        read_only_fields = ("creado_en", "actualizado_en")


class RegistroDietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDieta
        fields = [
            "id",
            "admision",
            "tiempo",
            "dieta",
            "observaciones",
            "registrado_por",
            "registrado_en",
        ]
        read_only_fields = ("registrado_en",)


class OrdenMedicaEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenMedicaEvento
        fields = [
            "id",
            "orden",
            "estado",
            "comentario",
            "creado_por",
            "creado_en",
        ]
        read_only_fields = ("creado_en",)


class OrdenMedicaSerializer(serializers.ModelSerializer):
    eventos = OrdenMedicaEventoSerializer(many=True, read_only=True)

    class Meta:
        model = OrdenMedica
        fields = [
            "id",
            "admision",
            "titulo",
            "descripcion",
            "estado",
            "prioridad",
            "observaciones",
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
            "cerrado_en",
            "cerrado_por",
            "eventos",
        ]
        read_only_fields = ("creado_en", "actualizado_en")
