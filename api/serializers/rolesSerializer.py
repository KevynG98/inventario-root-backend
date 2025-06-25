from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.rolesModel import Role, ClaveEspecial
from ..utils.claveSecreta import generar_clave_especial

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class AsignarRolSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()
    clave = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        user_id = validated_data['user_id']
        role_id = validated_data['role_id']
        clave_proporcionada = validated_data.get('clave', '').strip()

        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)

        # Asignar rol si aún no lo tiene
        if not user.roles.filter(id=role.id).exists():
            user.roles.add(role)

        clave_final = None
        if role.id == 2:  # Solo para rol "caja"
            if not hasattr(user, 'clave_especial'):
                clave_final = clave_proporcionada or generar_clave_especial()
                ClaveEspecial.objects.create(usuario=user, clave=clave_final)
            else:
                clave_final = user.clave_especial.clave

        return {
            'usuario': user.username,
            'rol_asignado': role.name,
            'clave': clave_final
        }