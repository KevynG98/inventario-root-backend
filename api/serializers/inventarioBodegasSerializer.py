from rest_framework import serializers
from ..models.inventarioBodegasModel import Bodegas, Cajero

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = '__all__'

class CajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cajero
        fields = '__all__'