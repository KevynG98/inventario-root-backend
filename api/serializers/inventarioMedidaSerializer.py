from rest_framework import serializers
from ..models.inventarioMedidaModel import Medida

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'
