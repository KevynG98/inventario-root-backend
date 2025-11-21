from rest_framework import serializers
from ..models.inventarioPrecioModel import PrecioInventario

class PrecioInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioInventario
        fields = '__all__'
