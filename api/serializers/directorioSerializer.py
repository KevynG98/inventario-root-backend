from rest_framework import serializers
from ..models.directorioModel import Directorio

class DirectorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directorio
        fields = '__all__'
