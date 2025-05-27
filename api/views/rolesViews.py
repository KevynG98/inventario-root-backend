from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from ..models.rolesModel import Role
from ..serializers.rolesSerializer import RoleSerializer, AsignarRolSerializer
from rest_framework import status

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def assign_role(request):
    username = request.data.get("username")
    role_name = request.data.get("role")

    if not username or not role_name:
        return Response({"error": "Both 'username' and 'role' are required"}, status=400)

    user = User.objects.filter(username=username).first()
    if not user:
        return Response({"error": "User not found"}, status=404)

    role, created = Role.objects.get_or_create(name=role_name)
    role.users.add(user)

    return Response({"message": f"Role '{role_name}' assigned to {user.username}"}, status=200)


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def create_role(request):
    role_name = request.data.get("name")

    if not role_name:
        return Response({"error": "Role name is required"}, status=400)

    role, created = Role.objects.get_or_create(name=role_name)

    if created:
        return Response({"message": f"Role '{role_name}' created successfully"}, status=201)
    else:
        return Response({"error": "Role already exists"}, status=400)
    
@api_view(['POST'])
def asignar_rol(request):
    serializer = AsignarRolSerializer(data=request.data)
    if serializer.is_valid():
        resultado = serializer.save()
        return Response(resultado, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)