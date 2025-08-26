from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction

from api.utils.pagination import CustomPageNumberPagination
from ..models.entradasModel import Entrada
from ..serializers.entradasSerializer import EntradaSerializer
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU


search_fecha = openapi.Parameter('fecha', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING)
search_bodega = openapi.Parameter('bodega', openapi.IN_QUERY, type=openapi.TYPE_STRING)
search_tipo = openapi.Parameter('tipo', openapi.IN_QUERY, type=openapi.TYPE_STRING)


@swagger_auto_schema(method='get', tags=['Bodegas - Entradas'], manual_parameters=[search_fecha, search_bodega, search_tipo], operation_description='Listar entradas con filtros y paginación')
@api_view(['GET'])
def listar_entradas(request):
    qs = Entrada.objects.all().order_by('-id')
    f_fecha = request.GET.get('fecha')
    f_bodega = request.GET.get('bodega')
    f_tipo = request.GET.get('tipo')
    if f_fecha:
        qs = qs.filter(created_at__date=f_fecha)
    if f_bodega:
        qs = qs.filter(bodega__icontains=f_bodega)
    if f_tipo:
        qs = qs.filter(tipo_entrada=f_tipo)

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = EntradaSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Bodegas - Entradas'], request_body=EntradaSerializer, operation_description='Crear nueva entrada (estado: No Aplicada)')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crear_entrada(request):
    serializer = EntradaSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        entrada = serializer.save()
        return Response(EntradaSerializer(entrada).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Bodegas - Entradas'], operation_description='Obtener entrada por ID')
@api_view(['GET'])
def obtener_entrada(request, pk):
    try:
        entrada = Entrada.objects.get(pk=pk)
        return Response(EntradaSerializer(entrada).data)
    except Entrada.DoesNotExist:
        return Response({'error': 'Entrada no encontrada'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='post', tags=['Bodegas - Entradas'], operation_description='Aplicar entrada: suma existencias a bodega y marca como Aplicada')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def aplicar_entrada(request, pk):
    try:
        entrada = Entrada.objects.select_for_update().get(pk=pk)
    except Entrada.DoesNotExist:
        return Response({'error': 'Entrada no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if entrada.estado == 'aplicada':
        return Response({'message': 'La entrada ya está aplicada'}, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar stock por item
    for item in entrada.items.all():
        sku_code = item.sku
        try:
            sku_obj = InventarioSKU.objects.get(codigo_sku=sku_code)
        except InventarioSKU.DoesNotExist:
            return Response({'error': f'SKU {sku_code} no existe'}, status=status.HTTP_400_BAD_REQUEST)

        bodega_sku, _ = BodegaSKU.objects.get_or_create(sku=sku_obj, nombre_bodega=entrada.bodega, defaults={'cantidad': 0})
        bodega_sku.cantidad = int(bodega_sku.cantidad + int(item.cantidad))
        bodega_sku.save()

    entrada.estado = 'aplicada'
    # Registrar usuario que aplica
    user = getattr(request, 'user', None)
    username = None
    if user and getattr(user, 'is_authenticated', False):
        username = user.username
    else:
        username = request.headers.get('X-User') or None
    entrada.aplicado_por = username
    entrada.save()

    return Response({'message': 'Entrada aplicada', 'entrada': EntradaSerializer(entrada).data}, status=status.HTTP_200_OK)



@swagger_auto_schema(method='put', tags=['Bodegas - Entradas'], request_body=EntradaSerializer, operation_description='Actualizar entrada (solo si no aplicada)')
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_entrada(request, pk):
    try:
        entrada = Entrada.objects.get(pk=pk)
    except Entrada.DoesNotExist:
        return Response({'error': 'Entrada no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EntradaSerializer(entrada, data=request.data, context={'request': request})
    if serializer.is_valid():
        entrada = serializer.save()
        return Response(EntradaSerializer(entrada).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', tags=['Bodegas - Entradas'], operation_description='Eliminar entrada (solo si no aplicada)')
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_entrada(request, pk):
    try:
        entrada = Entrada.objects.get(pk=pk)
    except Entrada.DoesNotExist:
        return Response({'error': 'Entrada no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if entrada.estado == 'aplicada':
        return Response({'error': 'No se puede eliminar una entrada aplicada'}, status=status.HTTP_400_BAD_REQUEST)

    entrada.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
