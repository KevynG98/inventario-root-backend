from django.db import transaction
from rest_framework import serializers

from .models import DetalleSolicitud, Solicitud


class DetalleSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSolicitud
        fields = [
            "id",
            "sku",
            "descripcion",
            "cantidad",
            "enviada",
            "comentario",
        ]

    def validate_cantidad(self, value: int) -> int:
        if value is None or value < 0:
            raise serializers.ValidationError("La cantidad debe ser un entero mayor o igual a cero.")
        return value

    def validate_enviada(self, value):
        if value is None:
            return value
        if value < 0:
            raise serializers.ValidationError("La cantidad enviada no puede ser negativa.")
        return value


class SolicitudSerializer(serializers.ModelSerializer):
    detalle = DetalleSolicitudSerializer(many=True)

    class Meta:
        model = Solicitud
        fields = [
            "id",
            "fecha",
            "admision",
            "paciente",
            "area",
            "habitacion",
            "bodega_origen",
            "bodega_destino",
            "estatus",
            "detalle",
        ]
        read_only_fields = ("fecha",)

    def validate(self, attrs):
        detalle = attrs.get("detalle", [])
        if not detalle:
            raise serializers.ValidationError({"detalle": "Debe incluir al menos un SKU en la solicitud."})
        return attrs

    def create(self, validated_data):
        detalle_data = validated_data.pop("detalle", [])
        with transaction.atomic():
            solicitud = Solicitud.objects.create(**validated_data)
            self._create_detalle(solicitud, detalle_data)
        return solicitud

    def update(self, instance, validated_data):
        detalle_data = validated_data.pop("detalle", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        with transaction.atomic():
            instance.save()
            if detalle_data is not None:
                instance.detalle.all().delete()
                self._create_detalle(instance, detalle_data)
        return instance

    def _create_detalle(self, solicitud: Solicitud, detalle_data):
        detalle_instances = [
            DetalleSolicitud(
                solicitud=solicitud,
                sku=item["sku"],
                descripcion=item.get("descripcion", ""),
                cantidad=item.get("cantidad", 0),
                enviada=item.get("enviada"),
                comentario=item.get("comentario"),
            )
            for item in detalle_data
        ]
        DetalleSolicitud.objects.bulk_create(detalle_instances)
