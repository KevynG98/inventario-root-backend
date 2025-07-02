from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioSegurosModel import Seguros
from ..serializers.inventarioSegurosSerializer import SegurosSerializer


@swagger_auto_schema(method='get', operation_summary="Listar seguros", tags=["inventario-seguro"])
@api_view(['GET'])
def listar_seguros(request):
    """
    Lista todos los seguros activos con paginación.
    """
    seguros = Seguros.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(seguros, request)
    serializer = SegurosSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', request_body=SegurosSerializer, operation_summary="Crear seguro", tags=["inventario-seguro"])
@api_view(['POST'])
def crear_seguros(request):
    """
    Crea un nuevo seguro.
    """
    serializer = SegurosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=SegurosSerializer, operation_summary="Actualizar seguro", tags=["inventario-seguro"])
@api_view(['PUT'])
def actualizar_seguros(request, pk):
    """
    Actualiza un seguro existente por ID.
    """
    try:
        seguro = Seguros.objects.get(pk=pk)
    except Seguros.DoesNotExist:
        return Response({'error': 'Seguro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SegurosSerializer(seguro, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', operation_summary="Eliminar seguro (soft delete)", tags=["inventario-seguro"])
@api_view(['DELETE'])
def eliminar_seguros(request, pk):
    """
    Marca como inactivo (soft delete) un seguro por su ID.
    """
    try:
        seguro = Seguros.objects.get(pk=pk)
    except Seguros.DoesNotExist:
        return Response({'error': 'Seguro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    seguro.is_active = False
    seguro.save()
    return Response({'mensaje': 'Seguro eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', operation_summary="Obtener seguro por ID", tags=["inventario-seguro"])
@api_view(['GET'])
def obtener_seguros(request, pk):
    """
    Devuelve los datos de un seguro específico por su ID.
    """
    try:
        seguro = Seguros.objects.get(pk=pk)
        serializer = SegurosSerializer(seguro)
        return Response(serializer.data)
    except Seguros.DoesNotExist:
        return Response({'error': 'Seguro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
