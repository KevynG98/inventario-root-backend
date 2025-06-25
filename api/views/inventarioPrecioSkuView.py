from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..models.inventarioPrecioSkuModel import PrecioSKU
from ..serializers.inventarioPrecioSkuSerializer import PrecioSKUSerializer


@swagger_auto_schema(method='get', operation_summary="Listar precios de SKUs", tags=["inventario-precio"])
@api_view(['GET'])
def listar_precios(request):
    """
    Lista todos los precios activos de SKUs.
    """
    precios = PrecioSKU.objects.filter(is_active=True)
    serializer = PrecioSKUSerializer(precios, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=PrecioSKUSerializer, operation_summary="Crear nuevo precio", tags=["inventario-precio"])
@api_view(['POST'])
def crear_precio(request):
    """
    Crea un nuevo registro de precio para un SKU.
    """
    print(request.data)
    serializer = PrecioSKUSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=PrecioSKUSerializer, operation_summary="Actualizar precio de SKU", tags=["inventario-precio"])
@api_view(['PUT'])
def actualizar_precio(request, pk):
    """
    Actualiza un precio de SKU por ID.
    """
    try:
        precio = PrecioSKU.objects.get(pk=pk, is_active=True)
    except PrecioSKU.DoesNotExist:
        return Response({"error": "Precio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    print("🔍 Datos recibidos:", request.data)
    serializer = PrecioSKUSerializer(precio, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("❌ Errores del serializer:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', operation_summary="Eliminar precio (soft delete)", tags=["inventario-precio"])
@api_view(['DELETE'])
def eliminar_precio(request, pk):
    """
    Elimina (soft delete) un precio de SKU por ID.
    """
    try:
        precio = PrecioSKU.objects.get(pk=pk, is_active=True)
        precio.is_active = False
        precio.save()
        return Response({"message": "Precio eliminado (soft delete)"}, status=status.HTTP_200_OK)
    except PrecioSKU.DoesNotExist:
        return Response({"error": "Precio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
