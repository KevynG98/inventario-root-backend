from rest_framework import serializers
from django.contrib.auth.models import User
from ..serializers.rolesSerializer import RoleSerializer  # Importa el serializer de roles

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'roles']
        extra_kwargs = {'password': {'write_only': True}}  # Para no exponer la contraseña en la respuesta