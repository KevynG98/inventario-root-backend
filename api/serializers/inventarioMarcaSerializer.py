from rest_framework import serializers
from ..models.inventarioMarcaModel import Marca

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'
