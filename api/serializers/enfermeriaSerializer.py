from decimal import Decimal, InvalidOperation

from django.utils import timezone
from rest_framework import serializers

from ..models.enfermeriaModel import (
    AdmisionMedicoTratante,
    AntecedenteClinico,
    ControlMedicamento,
    ControlMedicamentoRegistro,
    EvolucionClinica,
    HistoriaEnfermedad,
    NotaEnfermeria,
    OrdenMedica,
    OrdenMedicaEvento,
    RegistroDieta,
    SignoVitalEmergencia,
    SignoVitalEncamamiento,
    IngestaExcretaDia,
    IngestaExcretaRegistro,
    INGESTA_COLUMN_IDS,
    EXCRETA_COLUMN_IDS,
    INGESTA_EXCRETA_COLUMN_IDS,
    default_row_values,
    SolicitudMedicamento,
    SolicitudMedicamentoItem,
)


def _numeric_value(value):
    if value in (None, "", " "):
        return Decimal("0")
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    if isinstance(value, str):
        normalized = value.replace(",", ".")
        try:
            return Decimal(normalized)
        except (InvalidOperation, ValueError):
            return Decimal("0")
    return Decimal("0")


def _normalize_valores(data):
    normalized = default_row_values()
    if isinstance(data, dict):
        for key in INGESTA_EXCRETA_COLUMN_IDS:
            if key in data:
                normalized[key] = data[key]
    return normalized


def _calculate_totals(registros):
    column_totals = {key: Decimal("0") for key in INGESTA_EXCRETA_COLUMN_IDS}
    for registro in registros:
        valores = registro.valores or {}
        for key in INGESTA_EXCRETA_COLUMN_IDS:
            column_totals[key] += _numeric_value(valores.get(key))

    total_ingesta = sum(column_totals[key] for key in INGESTA_COLUMN_IDS)
    total_excreta = sum(column_totals[key] for key in EXCRETA_COLUMN_IDS)
    balance = total_ingesta - total_excreta
    return {
        "column_totals": {key: str(column_totals[key]) for key in column_totals},
        "total_ingesta": str(total_ingesta),
        "total_excreta": str(total_excreta),
        "balance": str(balance),
    }


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


class IngestaExcretaRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestaExcretaRegistro
        fields = [
            "id",
            "slot",
            "turno",
            "valores",
            "actualizado_por",
            "actualizado_en",
        ]
        read_only_fields = ("id", "turno", "actualizado_por", "actualizado_en")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["valores"] = _normalize_valores(instance.valores or {})
        return data


class IngestaExcretaDiaSerializer(serializers.ModelSerializer):
    registros = IngestaExcretaRegistroSerializer(many=True, required=False)
    resumen_totales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IngestaExcretaDia
        fields = [
            "id",
            "admision",
            "fecha",
            "columnas_personalizadas",
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
            "registros",
            "resumen_totales",
        ]
        read_only_fields = (
            "creado_por",
            "actualizado_por",
            "creado_en",
            "actualizado_en",
        )

    def _clean_columnas(self, data):
        if not isinstance(data, dict):
            return {}
        limpio = {}
        for key, value in data.items():
            if key in INGESTA_EXCRETA_COLUMN_IDS:
                limpio[key] = str(value).strip() if value is not None else ""
        return limpio

    def _resolve_username(self):
        request = self.context.get("request")
        if not request:
            return None
        if request.user and request.user.is_authenticated:
            return request.user.username
        return request.headers.get("X-User")

    def _update_registros(self, instance, registros_data):
        if not isinstance(registros_data, list):
            return

        instance.ensure_registros()
        registros_existentes = {
            registro.slot: registro for registro in instance.registros.all()
        }
        username = self._resolve_username()
        now = timezone.now()
        to_update = []

        for payload in registros_data:
            slot = payload.get("slot")
            if not slot:
                continue
            registro = registros_existentes.get(slot)
            if not registro:
                continue

            valores = _normalize_valores(payload.get("valores", {}))
            registro.valores = valores
            registro.actualizado_en = now
            if username:
                registro.actualizado_por = username
            to_update.append(registro)

        if to_update:
            IngestaExcretaRegistro.objects.bulk_update(
                to_update,
                ["valores", "actualizado_por", "actualizado_en"]
            )

    def create(self, validated_data):
        registros_data = validated_data.pop("registros", None)
        columnas = self._clean_columnas(
            validated_data.get("columnas_personalizadas", {})
        )
        validated_data["columnas_personalizadas"] = columnas
        instance = IngestaExcretaDia.objects.create(**validated_data)
        instance.ensure_registros()
        if registros_data:
            self._update_registros(instance, registros_data)
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        registros_data = validated_data.pop("registros", None)
        if "columnas_personalizadas" in validated_data:
            instance.columnas_personalizadas = self._clean_columnas(
                validated_data.get("columnas_personalizadas", {})
            )
        if "fecha" in validated_data:
            instance.fecha = validated_data["fecha"]
        instance.save()
        instance.ensure_registros()
        if registros_data is not None:
            self._update_registros(instance, registros_data)
        instance.refresh_from_db()
        return instance

    def get_resumen_totales(self, obj):
        obj.ensure_registros()
        resumen = _calculate_totals(obj.registros.all())
        return resumen

    def to_representation(self, instance):
        instance.ensure_registros()
        instance.refresh_from_db()
        return super().to_representation(instance)


class SolicitudMedicamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudMedicamentoItem
        fields = [
            "id",
            "orden_medica_id",
            "sku",
            "descripcion",
            "categoria",
            "subcategoria",
            "cantidad_pedida",
            "cantidad_enviada",
            "cantidad_recibida",
            "cantidad_devuelta",
            "comentario_far",
            "comentario_enfermeria",
            "recibido",
            "devuelto",
            "traslado_devolucion",
            "devuelto_en",
            "devuelto_por",
            "usuario_traslado_devolucion",
            "departamento_traslado_devolucion",
        ]
        read_only_fields = (
            "cantidad_enviada",
            "cantidad_recibida",
            "cantidad_devuelta",
            "comentario_far",
            "recibido",
            "devuelto",
            "traslado_devolucion",
            "devuelto_en",
            "devuelto_por",
            "usuario_traslado_devolucion",
            "departamento_traslado_devolucion",
        )

    def validate(self, attrs):
        if attrs.get("cantidad_pedida", 0) < 0:
            raise serializers.ValidationError("La cantidad pedida debe ser mayor o igual a cero.")
        return attrs


class SolicitudMedicamentoSerializer(serializers.ModelSerializer):
    items = SolicitudMedicamentoItemSerializer(many=True, required=False)
    estatus_display = serializers.CharField(source="get_estatus_display", read_only=True)
    traslado_recibo = serializers.PrimaryKeyRelatedField(read_only=True)
    salida_cuenta = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SolicitudMedicamento
        fields = [
            "id",
            "admision",
            "bodega_origen",
            "bodega_destino",
            "comentarios",
            "estatus",
            "estatus_display",
            "creado_por",
            "actualizado_por",
            "enviado_por",
            "recibido_por",
            "cargado_por",
            "fecha_creacion",
            "fecha_actualizacion",
            "fecha_envio",
            "fecha_recibido",
            "fecha_cargado_ec",
            "traslado_recibo",
            "salida_cuenta",
            "items",
        ]
        read_only_fields = (
            "creado_por",
            "actualizado_por",
            "enviado_por",
            "recibido_por",
            "cargado_por",
            "fecha_creacion",
            "fecha_actualizacion",
            "fecha_envio",
            "fecha_recibido",
            "fecha_cargado_ec",
            "traslado_recibo",
            "salida_cuenta",
        )

    def _resolve_username(self):
        request = self.context.get("request")
        if not request:
            return None
        if request.user and request.user.is_authenticated:
            return request.user.username
        return request.headers.get("X-User")

    def _assert_editable(self, instance: SolicitudMedicamento):
        if instance.estatus not in (
            SolicitudMedicamento.Estados.PENDIENTE_ENVIAR,
        ):
            raise serializers.ValidationError(
                "Solo se pueden editar solicitudes en estado Pendiente de Enviar."
            )

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        username = self._resolve_username()
        if username:
            validated_data.setdefault("creado_por", username)
            validated_data.setdefault("actualizado_por", username)
        solicitud = SolicitudMedicamento.objects.create(**validated_data)
        for item in items_data:
            SolicitudMedicamentoItem.objects.create(solicitud=solicitud, **item)
        return solicitud

    def update(self, instance, validated_data):
        self._assert_editable(instance)
        items_data = validated_data.pop("items", None)
        username = self._resolve_username()
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if username:
            instance.actualizado_por = username
        instance.save()

        if items_data is not None:
            existing_items = {item.id: item for item in instance.items.all()}
            incoming_ids = []
            for item_payload in items_data:
                item_id = item_payload.get("id")
                if item_id and item_id in existing_items:
                    item_instance = existing_items[item_id]
                    for field, value in item_payload.items():
                        if field == "id":
                            continue
                        setattr(item_instance, field, value)
                    item_instance.save()
                    incoming_ids.append(item_id)
                else:
                    new_item_payload = {k: v for k, v in item_payload.items() if k != "id"}
                    item = SolicitudMedicamentoItem.objects.create(
                        solicitud=instance, **new_item_payload
                    )
                    incoming_ids.append(item.id)
            # eliminar items que no están en payload
            for item_id, item in existing_items.items():
                if item_id not in incoming_ids:
                    item.delete()

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Filtrar ítems devueltos para no mostrarlos en lista activa
        data["items"] = [
            item for item in data.get("items", []) if not item.get("devuelto")
        ]
        return data


class EvolucionClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolucionClinica
        fields = [
            "id",
            "admision",
            "resumen",
            "contenido",
            "medico_nombre",
            "medico_colegiado",
            "creado_por_username",
            "actualizado_por_username",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = (
            "medico_nombre",
            "medico_colegiado",
            "creado_por_username",
            "actualizado_por_username",
            "creado_en",
            "actualizado_en",
        )


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
