from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction

from api.utils.pagination import CustomPageNumberPagination
from ..models.salidasModel import Salida, SalidaItem
from ..serializers.salidasSerializer import SalidaSerializer, SalidaItemSerializer
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU


search_fecha = openapi.Parameter('fecha', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING)
search_bodega = openapi.Parameter('bodega', openapi.IN_QUERY, type=openapi.TYPE_STRING)
search_tipo = openapi.Parameter('tipo', openapi.IN_QUERY, type=openapi.TYPE_STRING)


@swagger_auto_schema(method='get', tags=['Bodegas - Salidas'], manual_parameters=[search_fecha, search_bodega, search_tipo], operation_description='Listar salidas con filtros y paginación')
@api_view(['GET'])
def listar_salidas(request):
    qs = Salida.objects.all().order_by('-id')
    f_fecha = request.GET.get('fecha')
    f_bodega = request.GET.get('bodega')
    f_tipo = request.GET.get('tipo')
    if f_fecha:
        qs = qs.filter(created_at__date=f_fecha)
    if f_bodega:
        qs = qs.filter(bodega__icontains=f_bodega)
    if f_tipo:
        qs = qs.filter(tipo_salida=f_tipo)

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = SalidaSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Bodegas - Salidas'], request_body=SalidaSerializer, operation_description='Crear (aplicar) una salida — resta existencias y registra salida')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_salida(request):
    try:
        serializer = SalidaSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        items = data.pop('items', [])

        if not items:
            return Response({'error': 'Debe agregar al menos un SKU a la salida.'}, status=status.HTTP_400_BAD_REQUEST)

        if any(not str(it.get('sku', '')).strip() for it in items):
            return Response({'error': 'Todos los ítems de la salida deben tener un SKU válido.'}, status=status.HTTP_400_BAD_REQUEST)
        # Registrar usuario creador y aplicado_por (salida se aplica al crear)
        user = getattr(request, 'user', None)
        username = None
        if user and getattr(user, 'is_authenticated', False):
            username = user.username
        else:
            username = request.headers.get('X-User') or None
        salida = Salida.objects.create(usuario=username, aplicado_por=username, **data)

        # restar existencias
        for item in items:
            item_ser = SalidaItemSerializer(data=item)
            item_ser.is_valid(raise_exception=True)
            it = item_ser.validated_data
            sku_code = it.get('sku')
            cantidad = int(it.get('cantidad'))
            try:
                sku_obj = InventarioSKU.objects.get(codigo_sku=sku_code)
            except InventarioSKU.DoesNotExist:
                transaction.set_rollback(True)
                return Response({'error': f'SKU {sku_code} no existe'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                bodega_sku = BodegaSKU.objects.select_for_update().get(sku=sku_obj, nombre_bodega=salida.bodega)
            except BodegaSKU.DoesNotExist:
                transaction.set_rollback(True)
                return Response({'error': f'No hay stock de {sku_code} en bodega {salida.bodega}'}, status=status.HTTP_400_BAD_REQUEST)

            if bodega_sku.cantidad < cantidad:
                transaction.set_rollback(True)
                return Response({'error': f'Stock insuficiente para {sku_code}. Disponible: {bodega_sku.cantidad}, requerido: {cantidad}'}, status=status.HTTP_400_BAD_REQUEST)

            bodega_sku.cantidad = bodega_sku.cantidad - cantidad
            bodega_sku.save()

            # crear item de salida
            SalidaItem.objects.create(salida=salida, **it)

        return Response(SalidaSerializer(salida).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        transaction.set_rollback(True)
        # Devuelve mensaje claro al frontend en lugar de 500 genérico
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Bodegas - Salidas'], operation_description='Obtener salida por ID')
@api_view(['GET'])
def obtener_salida(request, pk):
    try:
        salida = Salida.objects.get(pk=pk)
        return Response(SalidaSerializer(salida).data)
    except Salida.DoesNotExist:
        return Response({'error': 'Salida no encontrada'}, status=status.HTTP_404_NOT_FOUND)
