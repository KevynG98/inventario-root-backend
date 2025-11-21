from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.rolesModel import Role
from ..serializers.rolesSerializer import RoleSerializer


def _resolve_role(identifier):
    """
    Accepta un id numérico o un nombre de rol y devuelve el Role correspondiente.
    """
    if identifier is None:
        return None
    role = None
    try:
        role = Role.objects.filter(id=int(identifier)).first()
    except (ValueError, TypeError):
        role = Role.objects.filter(name=identifier).first()
    if not role:
        role = Role.objects.filter(name=identifier).first()
    return role


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def listar_roles(request):
    roles = Role.objects.all().order_by('id')
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def crear_rol(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        request.descripcion = f"Se creó el rol '{serializer.data.get('name')}'"
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def asignar_rol(request):
    username = request.data.get('username')
    role_input = request.data.get('role')

    if not username or not role_input:
        return Response({'error': 'username y role son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    role = _resolve_role(role_input)
    if not role:
        return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    role.users.add(user)
    request.descripcion = f"Se asignó el rol '{role.name}' al usuario '{user.username}'"
    return Response({'message': 'Rol asignado correctamente'}, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def desasignar_rol(request):
    username = request.data.get('username')
    role_input = request.data.get('role')

    if not username or not role_input:
        return Response({'error': 'username y role son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    role = _resolve_role(role_input)
    if not role:
        return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    role.users.remove(user)
    request.descripcion = f"Se desasignó el rol '{role.name}' del usuario '{user.username}'"
    return Response({'message': 'Rol desasignado correctamente'}, status=status.HTTP_200_OK)
