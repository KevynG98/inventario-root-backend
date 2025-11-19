from rest_framework import serializers
from ..models.inventariosSkuModel import InventarioSKU

class InventarioSKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioSKU
        fields = '__all__'
