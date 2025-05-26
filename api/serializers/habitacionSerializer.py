from rest_framework import serializers
from django.db.models import Max
from api.models.habitacionModel import (
    Habitacion
)

class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id', 'codigo', 'area', 'estado', 'admision', 'paciente', 'nivel', 'observacion']

    def validate_admision(self, value):
        if value is not None:
            qs = Habitacion.objects.filter(admision=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Esta admisión ya está asignada a otra habitación.")
        return value