from rest_framework import serializers
from django.contrib.auth.models import User
from ..serializers.rolesSerializer import RoleSerializer  # Importa el serializer de roles

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'roles', 'is_active']  # 🔥 Agregado aquí