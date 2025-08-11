from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioMedidaModel import Medida
from ..serializers.inventarioMedidaSerializer import MedidaSerializer# 👈 CORREGIDO

@swagger_auto_schema(method='get', tags=['Inventario - Medidas'], operation_description="Listar medidas activas con paginación")
@api_view(['GET'])
def listar_medidas(request):
    medidas = Medida.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(medidas, request)
    serializer = MedidaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario - Medidas'], operation_description="Crear una nueva medida", request_body=MedidaSerializer)
@api_view(['POST'])
def crear_medida(request):
    serializer = MedidaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario - Medidas'], operation_description="Actualizar una medida por ID", request_body=MedidaSerializer)
@api_view(['PUT'])
def actualizar_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MedidaSerializer(medida, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Inventario - Medidas'], operation_description="Eliminar (soft delete) una medida por ID")
@api_view(['DELETE'])
def eliminar_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    medida.is_active = False
    medida.save()
    return Response({'mensaje': 'Medida eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Inventario - Medidas'], operation_description="Obtener una medida por ID")
@api_view(['GET'])
def obtener_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
        serializer = MedidaSerializer(medida)
        return Response(serializer.data)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)
