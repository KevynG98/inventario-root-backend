from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioPrincipiosModel import Principios
from ..serializers.inventarioPrincipiosSerializer import PrincipiosSerializer

@swagger_auto_schema(method='get', tags=['Inventario - Marcas'], operation_description="Listar marcas activas con paginación")
@api_view(['GET'])
def listar_principios(request):
    marcas = Principios.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(marcas, request)
    serializer = PrincipiosSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario - Marcas'], operation_description="Crear una nueva marca", request_body=PrincipiosSerializer)
@api_view(['POST'])
def crear_principios(request):
    serializer = PrincipiosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario - Marcas'], operation_description="Actualizar una marca por ID", request_body=PrincipiosSerializer)
@api_view(['PUT'])
def actualizar_principios(request, pk):
    try:
        marca = Principios.objects.get(pk=pk)
    except Principios.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PrincipiosSerializer(marca, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Inventario - Marcas'], operation_description="Eliminar (soft delete) una marca por ID")
@api_view(['DELETE'])
def eliminar_principios(request, pk):
    try:
        marca = Principios.objects.get(pk=pk)
    except Principios.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    marca.is_active = False
    marca.save()
    return Response({'mensaje': 'Marca eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Inventario - Marcas'], operation_description="Obtener una marca por ID")
@api_view(['GET'])
def obtener_principios(request, pk):
    try:
        marca = Principios.objects.get(pk=pk)
        serializer = PrincipiosSerializer(marca)
        return Response(serializer.data)
    except Principios.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)
