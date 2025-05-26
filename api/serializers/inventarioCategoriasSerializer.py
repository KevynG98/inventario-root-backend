from rest_framework import serializers
from ..models.inventarioCategoriasModel import CategoriaInventario

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaInventario
        fields = '__all__'
