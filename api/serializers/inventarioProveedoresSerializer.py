from rest_framework import serializers
from ..models.inventarioProveedoresModel import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
