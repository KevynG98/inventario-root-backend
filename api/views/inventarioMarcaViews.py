from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioMarcaModel import Marca
from ..serializers.inventarioMarcaSerializer import MarcaSerializer

@swagger_auto_schema(method='get', tags=['Inventario - Marcas'], operation_description="Listar marcas activas con paginación")
@api_view(['GET'])
def listar_marcas(request):
    marcas = Marca.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(marcas, request)
    serializer = MarcaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario - Marcas'], operation_description="Crear una nueva marca", request_body=MarcaSerializer)
@api_view(['POST'])
def crear_marca(request):
    serializer = MarcaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario - Marcas'], operation_description="Actualizar una marca por ID", request_body=MarcaSerializer)
@api_view(['PUT'])
def actualizar_marca(request, pk):
    try:
        marca = Marca.objects.get(pk=pk)
    except Marca.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MarcaSerializer(marca, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Inventario - Marcas'], operation_description="Eliminar (soft delete) una marca por ID")
@api_view(['DELETE'])
def eliminar_marca(request, pk):
    try:
        marca = Marca.objects.get(pk=pk)
    except Marca.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    marca.is_active = False
    marca.save()
    return Response({'mensaje': 'Marca eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Inventario - Marcas'], operation_description="Obtener una marca por ID")
@api_view(['GET'])
def obtener_marca(request, pk):
    try:
        marca = Marca.objects.get(pk=pk)
        serializer = MarcaSerializer(marca)
        return Response(serializer.data)
    except Marca.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)
