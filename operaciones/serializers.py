from rest_framework import serializers

from .models import Operacion


class OperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacion
        fields = [
            "id",
            "fecha",
            "dia",
            "hora",
            "paciente",
            "edad",
            "especialidad",
            "procedimiento",
            "cirujano1",
            "cirujano2",
            "cirujano3",
            "anestesiologo",
            "pediatra",
            "seguro",
            "material",
            "comentarios",
            "estatus",
            "historial",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ("historial", "creado_en", "actualizado_en")

    def create(self, validated_data):
        validated_data.setdefault("estatus", Operacion.Estatus.PROGRAMADO)
        return super().create(validated_data)
