from rest_framework import serializers
from ..models.inventarioCategoriasModel import CategoriaInventario, SubcategoriaInventario

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoriaInventario
        fields = '__all__'
        
class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = SubcategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = CategoriaInventario
        fields = '__all__'