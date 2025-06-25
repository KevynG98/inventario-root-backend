from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from ..serializers.userSerializaer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({"error": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)

    user.last_login = timezone.now()
    user.save()

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    # ✅ Lógica de auditoría
    request.descripcion = f"🔐 Usuario '{user.username}' inició sesión"
    request.user = user

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error': 'El nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()  # ✅ Llama a create() y guarda el perfil

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'last_login': user.last_login,
                'date_joined': user.date_joined,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recent_users(request):
    # Obtener los 5 usuarios más recientes por fecha de último inicio de sesión
    users = User.objects.all().order_by('-last_login')[:5]
    user_data = [{'username': user.username, 'last_login': user.last_login} for user in users]
    
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_users_filted(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Opcional

    users = User.objects.exclude(roles__name__iexact='doctor').order_by('id').prefetch_related('roles')

    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def all_doctor_users(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Opcional

    users = User.objects.filter(roles__name__iexact='doctor').order_by('id')

    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def all_users(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # 🔥 Opcional: puedes quitarlo si ya está en settings.py

    users = User.objects.all().order_by('id')
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({"message": f"You are logged in as: {request.user.username}"})

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if hasattr(user, 'perfil'):
        user.perfil.estado = False
        user.perfil.save()
    user.is_active = False
    user.save()

    return Response({"message": "Usuario desactivado (soft delete)"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    user = get_object_or_404(User, id=id)

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Usuario actualizado correctamente',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    print("❌ Errores del serializer:", serializer.errors)  # <-- agrega esta línea para depurar
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_users(request):
    search_query = request.GET.get('q', '')
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Mismo tamaño que usas para paginación

    users = User.objects.filter(
        username__icontains=search_query
    ) | User.objects.filter(
        first_name__icontains=search_query
    ) | User.objects.filter(
        last_name__icontains=search_query
    ) | User.objects.filter(
        email__icontains=search_query
    )

    users = users.order_by('id').distinct()

    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_reset_password(request, id):
    user = get_object_or_404(User, id=id)

    new_password = request.data.get('password')

    if not new_password:
        return Response({'error': 'La nueva contraseña es requerida'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    # Elimina el token para cerrar la sesión
    request.user.auth_token.delete()
    # Esto lo recogerá el middleware para registrar el cierre de sesión
    request.descripcion = f"🚪 Usuario {user.username} cerró sesión"
    return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)