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

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data.get("email"))
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
        user = User(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', '')
        )
        user.set_password(serializer.validated_data['password'])  # Encripta la contraseña
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def recent_users(request):
    # Obtener los 5 usuarios más recientes por fecha de último inicio de sesión
    users = User.objects.all().order_by('-last_login')[:5]
    user_data = [{'username': user.username, 'last_login': user.last_login} for user in users]
    
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    user_data = [
        {
            'id': user.id, 
            'last_login': user.last_login, 
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'rol': [{'id': role.id, 'rol': role.name} for role in user.roles.all()]
        } for user in users]
    
    return Response(user_data, status=status.HTTP_200_OK)

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
