from rest_framework import serializers
from ..models.inventarioMedidaModel import Medida

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'
