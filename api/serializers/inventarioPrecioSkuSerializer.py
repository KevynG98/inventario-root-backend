from rest_framework import serializers
from ..models.inventarioPrecioSkuModel import PrecioSKU

class PrecioSKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioSKU
        fields = '__all__'
