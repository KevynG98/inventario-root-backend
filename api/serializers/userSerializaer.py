# serializers/userSerializer.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .perfilSerializer import PerfilSerializer
from .rolesSerializer import RoleSerializer
from api.models.perfilModel import Perfil  # ✅ Importación correcta del modelo Perfil

class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(required=False)
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'perfil', 'roles']

    def create(self, validated_data):
        perfil_data = validated_data.pop('perfil', {})
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()

        if perfil_data:
            Perfil.objects.update_or_create(user=user, defaults=perfil_data)

        return user

    def update(self, instance, validated_data):
        perfil_data = validated_data.pop('perfil', {})

        for attr, value in validated_data.items():
            if attr == 'password' and value:
                instance.set_password(value)
            elif attr != 'password':
                setattr(instance, attr, value)
        instance.save()

        # ✅ Actualizar campos individuales de perfil sin requerir todos
        perfil_obj, created = Perfil.objects.get_or_create(user=instance)
        for attr, value in perfil_data.items():
            setattr(perfil_obj, attr, value)
        perfil_obj.save()

        return instance

