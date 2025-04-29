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
    user = get_object_or_404(User, username=request.data.get("username"))
    if not user.check_password(request.data.get("password")):
        return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    user.last_login = timezone.now()
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error': 'El nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            is_active=serializer.validated_data.get('is_active', True),
        )

        
        password = serializer.validated_data.get('password', None)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        
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
    
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

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