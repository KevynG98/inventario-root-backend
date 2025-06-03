from rest_framework import serializers
from ..models.inventarioSegurosModel import Seguros

class SegurosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguros
        fields = '__all__'
