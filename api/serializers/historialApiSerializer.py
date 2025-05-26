from rest_framework import serializers
from ..models.historialApiModel import HistorialAPI

class HistorialAPISerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = HistorialAPI
        fields = '__all__'
