from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from django.utils import timezone

from api.utils.pagination import CustomPageNumberPagination
from ..models.trasladosModel import Traslado, TrasladoItem
from ..serializers.trasladosSerializer import TrasladoSerializer, TrasladoItemSerializer
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU


search_envio = openapi.Parameter('fecha_envio', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING)
search_recibido = openapi.Parameter('fecha_recibido', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING)
search_bodega_origen = openapi.Parameter('bodega_origen', openapi.IN_QUERY, type=openapi.TYPE_STRING)
search_estatus = openapi.Parameter('estatus', openapi.IN_QUERY, type=openapi.TYPE_STRING)


@swagger_auto_schema(method='get', tags=['Bodegas - Traslados'], manual_parameters=[search_envio, search_recibido, search_bodega_origen, search_estatus], operation_description='Listar traslados con filtros y paginación')
@api_view(['GET'])
def listar_traslados(request):
    qs = Traslado.objects.all().order_by('-id')
    f_envio = request.GET.get('fecha_envio')
    f_rec = request.GET.get('fecha_recibido')
    f_origen = request.GET.get('bodega_origen')
    f_est = request.GET.get('estatus')
    if f_envio:
        qs = qs.filter(fecha_envio__date=f_envio)
    if f_rec:
        qs = qs.filter(fecha_recibido__date=f_rec)
    if f_origen:
        qs = qs.filter(bodega_origen__icontains=f_origen)
    if f_est:
        qs = qs.filter(estatus=f_est)

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = TrasladoSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', tags=['Bodegas - Traslados'], request_body=TrasladoSerializer, operation_description='Crear traslado (Enviado): descuenta existencias de bodega origen')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_traslado(request):
    try:
        serializer = TrasladoSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        items = data.pop('items', [])
        # Determinar usuario
        user = getattr(request, 'user', None)
        username = None
        if user and getattr(user, 'is_authenticated', False):
            username = user.username
        else:
            username = request.headers.get('X-User') or None
        traslado = Traslado.objects.create(enviado_por=username, estatus='ENVIADO', **data)

        # Descontar existencias en bodega origen
        for item in items:
            item_ser = TrasladoItemSerializer(data=item)
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
                stock_origen = BodegaSKU.objects.select_for_update().get(sku=sku_obj, nombre_bodega=traslado.bodega_origen)
            except BodegaSKU.DoesNotExist:
                transaction.set_rollback(True)
                return Response({'error': f'No hay stock de {sku_code} en bodega {traslado.bodega_origen}'}, status=status.HTTP_400_BAD_REQUEST)

            if stock_origen.cantidad < cantidad:
                transaction.set_rollback(True)
                return Response({'error': f'Stock insuficiente para {sku_code}. Disponible: {stock_origen.cantidad}, requerido: {cantidad}'}, status=status.HTTP_400_BAD_REQUEST)

            stock_origen.cantidad = stock_origen.cantidad - cantidad
            stock_origen.save()

            TrasladoItem.objects.create(traslado=traslado, **it)

        return Response(TrasladoSerializer(traslado).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        transaction.set_rollback(True)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', tags=['Bodegas - Traslados'], operation_description='Marcar traslado como Recibido: suma existencias en bodega destino')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def recibir_traslado(request, pk):
    try:
        traslado = Traslado.objects.select_for_update().get(pk=pk)
    except Traslado.DoesNotExist:
        return Response({'error': 'Traslado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if traslado.estatus != 'ENVIADO':
        return Response({'error': 'Solo se pueden recibir traslados ENVIADO'}, status=status.HTTP_400_BAD_REQUEST)

    for item in traslado.items.all():
        sku_code = item.sku
        try:
            sku_obj = InventarioSKU.objects.get(codigo_sku=sku_code)
        except InventarioSKU.DoesNotExist:
            return Response({'error': f'SKU {sku_code} no existe'}, status=status.HTTP_400_BAD_REQUEST)

        stock_destino, _ = BodegaSKU.objects.get_or_create(sku=sku_obj, nombre_bodega=traslado.bodega_destino, defaults={'cantidad': 0})
        stock_destino.cantidad = int(stock_destino.cantidad + int(item.cantidad))
        stock_destino.save()

    traslado.estatus = 'RECIBIDO'
    traslado.fecha_recibido = timezone.now()
    user = getattr(request, 'user', None)
    username = None
    if user and getattr(user, 'is_authenticated', False):
        username = user.username
    else:
        username = request.headers.get('X-User') or traslado.recibido_por
    traslado.recibido_por = username
    traslado.save()

    return Response({'message': 'Traslado recibido', 'traslado': TrasladoSerializer(traslado).data}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', tags=['Bodegas - Traslados'], operation_description='Anular traslado: restaura stock en bodega origen si estaba ENVIADO')
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def anular_traslado(request, pk):
    try:
        traslado = Traslado.objects.select_for_update().get(pk=pk)
    except Traslado.DoesNotExist:
        return Response({'error': 'Traslado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if traslado.estatus == 'RECIBIDO':
        return Response({'error': 'No se puede anular un traslado recibido'}, status=status.HTTP_400_BAD_REQUEST)

    if traslado.estatus == 'ENVIADO':
        # Reponer stock en bodega origen
        for item in traslado.items.all():
            sku_code = item.sku
            try:
                sku_obj = InventarioSKU.objects.get(codigo_sku=sku_code)
            except InventarioSKU.DoesNotExist:
                return Response({'error': f'SKU {sku_code} no existe'}, status=status.HTTP_400_BAD_REQUEST)

            stock_origen, _ = BodegaSKU.objects.get_or_create(sku=sku_obj, nombre_bodega=traslado.bodega_origen, defaults={'cantidad': 0})
            stock_origen.cantidad = int(stock_origen.cantidad + int(item.cantidad))
            stock_origen.save()

    traslado.estatus = 'ANULADO'
    traslado.save()
    return Response({'message': 'Traslado anulado', 'traslado': TrasladoSerializer(traslado).data}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', tags=['Bodegas - Traslados'], operation_description='Obtener traslado por ID')
@api_view(['GET'])
def obtener_traslado(request, pk):
    try:
        traslado = Traslado.objects.get(pk=pk)
        return Response(TrasladoSerializer(traslado).data)
    except Traslado.DoesNotExist:
        return Response({'error': 'Traslado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
