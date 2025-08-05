from rest_framework import serializers
from ..models.inventarioPrincipiosModel import Principios

class PrincipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principios
        fields = '__all__'
