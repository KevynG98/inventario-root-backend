from rest_framework import serializers
from ..models.perfilModel import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        exclude = ['id', 'user']
