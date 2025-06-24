from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema # type: ignore
from drf_yasg import openapi # type: ignore

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioProveedoresModel import Proveedor
from ..serializers.inventarioProveedoresSerializer import ProveedorSerializer


@swagger_auto_schema(method='get', tags=['Inventario-Proveedores'], operation_description="Listar todos los proveedores activos con paginación")
@api_view(['GET'])
def listar_proveedores(request):
    proveedores = Proveedor.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(proveedores, request)
    serializer = ProveedorSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Inventario-Proveedores'], operation_description="Crear un nuevo proveedor", request_body=ProveedorSerializer)
@api_view(['POST'])
def crear_proveedor(request):
    serializer = ProveedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', tags=['Inventario-Proveedores'], operation_description="Actualizar proveedor existente", request_body=ProveedorSerializer)
@api_view(['PUT'])
def actualizar_proveedor(request, pk):
    try:
        proveedor = Proveedor.objects.get(pk=pk)
    except Proveedor.DoesNotExist:
        return Response({'error': 'Proveedor no encontrado'}, status=404)

    serializer = ProveedorSerializer(proveedor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Inventario-Proveedores'], operation_description="Obtener los datos de un proveedor por ID")
@api_view(['GET'])
def obtener_proveedor(request, pk):
    try:
        proveedor = Proveedor.objects.get(pk=pk)
        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)
    except Proveedor.DoesNotExist:
        return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='delete', tags=['Inventario-Proveedores'], operation_description="Eliminar (soft delete) un proveedor por ID")
@api_view(['DELETE'])
def eliminar_proveedor(request, pk):
    try:
        proveedor = Proveedor.objects.get(pk=pk)
    except Proveedor.DoesNotExist:
        return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    proveedor.is_active = False
    proveedor.save()
    return Response({'mensaje': 'Proveedor eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
