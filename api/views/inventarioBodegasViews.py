from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioBodegasModel import Bodegas
from ..serializers.inventarioBodegasSerializer import BodegaSerializer


@swagger_auto_schema(method='get', tags=['Inventario - Bodegas'], operation_description="Listar todas las bodegas activas con paginación")
@api_view(['GET'])
def listar_bodegas(request):
    bodegas = Bodegas.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(bodegas, request)
    serializer = BodegaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario - Bodegas'], operation_description="Crear una nueva bodega", request_body=BodegaSerializer)
@api_view(['POST'])
def crear_bodegas(request):
    serializer = BodegaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario - Bodegas'], operation_description="Actualizar una bodega por ID", request_body=BodegaSerializer)
@api_view(['PUT'])
def actualizar_bodegas(request, pk):
    try:
        bodega = Bodegas.objects.get(pk=pk)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Bodega no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BodegaSerializer(bodega, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Inventario - Bodegas'], operation_description="Eliminar (soft delete) una bodega por ID")
@api_view(['DELETE'])
def eliminar_bodegas(request, pk):
    try:
        bodega = Bodegas.objects.get(pk=pk)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Bodega no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    bodega.is_active = False
    bodega.save()
    return Response({'mensaje': 'Bodega eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', tags=['Inventario - Bodegas'], operation_description="Obtener una bodega por ID")
@api_view(['GET'])
def obtener_bodegas(request, pk):
    try:
        bodega = Bodegas.objects.get(pk=pk)
        serializer = BodegaSerializer(bodega)
        return Response(serializer.data)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Bodega no encontrada'}, status=status.HTTP_404_NOT_FOUND)
