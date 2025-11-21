from rest_framework import serializers
from ..models.inventarioProductoModel import InventarioProducto

class InventarioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioProducto
        fields = '__all__'
