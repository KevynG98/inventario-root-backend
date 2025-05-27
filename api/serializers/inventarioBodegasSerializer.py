from rest_framework import serializers
from ..models.inventarioBodegasModel import Bodegas

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = '__all__'
