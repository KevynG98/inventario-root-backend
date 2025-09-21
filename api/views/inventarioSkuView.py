from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU
from ..serializers.inventarioSkuSerializer import InventarioSKUSerializer, MovimientoBodegaSerializer


@swagger_auto_schema(method='get', operation_summary="Listar SKUs activos", tags=["inventario-sku"])
@api_view(['GET'])
def listar_skus(request):
    """
    Lista todos los SKUs activos con paginación.
    """
    skus = InventarioSKU.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(skus, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', request_body=InventarioSKUSerializer, operation_summary="Crear nuevo SKU", tags=["inventario-sku"])
@api_view(['POST'])
def crear_sku(request):
    """
    Crea un nuevo SKU con los datos proporcionados.
    """
    serializer = InventarioSKUSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # <- si falla, DRF responde 400 con el JSON de errores
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='get', operation_summary="Obtener SKU por ID", tags=["inventario-sku"])
@api_view(['GET'])
def obtener_sku(request, pk):
    """
    Retorna los datos de un SKU específico por su ID.
    """
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioSKUSerializer(sku)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=InventarioSKUSerializer, operation_summary="Actualizar SKU", tags=["inventario-sku"])
@api_view(['PUT'])
def actualizar_sku(request, pk):
    """
    Actualiza los datos de un SKU por su ID.
    """
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioSKUSerializer(sku, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', operation_summary="Eliminar SKU (soft delete)", tags=["inventario-sku"])
@api_view(['DELETE'])
def eliminar_sku(request, pk):
    """
    Marca como inactivo (soft delete) un SKU por su ID.
    """
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    sku.is_active = False
    sku.save()
    return Response({"mensaje": "SKU desactivado (soft delete)"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=MovimientoBodegaSerializer, operation_summary="Mover producto entre bodegas", tags=["inventario-sku"])
@api_view(['POST'])
def mover_producto(request):
    """
    Mueve un producto de una bodega a otra y actualiza las existencias.
    """
    serializer = MovimientoBodegaSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        sku = data['sku']
        origen = data['bodega_origen']
        destino = data['bodega_destino']
        cantidad = data['cantidad']

        try:
            stock_origen = BodegaSKU.objects.get(sku=sku, nombre_bodega=origen)
        except BodegaSKU.DoesNotExist:
            return Response({"error": "La bodega de origen no tiene stock del producto"}, status=400)

        if stock_origen.cantidad < cantidad:
            return Response({"error": "No hay suficiente stock en la bodega de origen"}, status=400)

        stock_origen.cantidad -= cantidad
        stock_origen.save()

        stock_destino, _ = BodegaSKU.objects.get_or_create(
            sku=sku, nombre_bodega=destino, defaults={'cantidad': 0}
        )
        stock_destino.cantidad += cantidad
        stock_destino.save()

        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='get', operation_summary="Listar SKUs con información de bodegas", tags=["inventario-sku"])
@api_view(['GET'])
def listar_skus_con_bodegas(request):
    """
    Lista SKUs con información relacionada a sus bodegas.
    """
    queryset = InventarioSKU.objects.prefetch_related('bodegas').order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_summary="Buscar SKUs con bodegas",
    tags=["inventario-sku"],
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description='Búsqueda libre por nombre, código SKU o código de barras', type=openapi.TYPE_STRING),
        openapi.Parameter('nombre', openapi.IN_QUERY, description='Filtrar por nombre (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('sku_codigo', openapi.IN_QUERY, description='Filtrar por código de SKU (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_barras', openapi.IN_QUERY, description='Filtrar por código de barras (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def buscar_skus_con_bodegas(request):
    """
    Busca SKUs (incluyendo sus bodegas) por nombre, código SKU o código de barras.
    Soporta búsqueda libre con ?q= y filtros específicos.
    Respuesta paginada.
    """
    queryset = InventarioSKU.objects.prefetch_related('bodegas').order_by('nombre')

    q = request.query_params.get('q')
    nombre = request.query_params.get('nombre')
    sku_codigo = request.query_params.get('sku_codigo')
    codigo_barras = request.query_params.get('codigo_barras')

    filtros = Q()
    if q:
        ql = q.strip()
        if ql:
            filtros |= Q(nombre__icontains=ql)
            filtros |= Q(codigo_sku__icontains=ql)
            # El campo en el modelo es 'barcode' (no 'codigo_barras')
            filtros |= Q(barcode__icontains=ql)
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if sku_codigo:
        filtros &= Q(codigo_sku__icontains=sku_codigo)
    if codigo_barras:
        filtros &= Q(barcode__icontains=codigo_barras)

    if filtros:
        queryset = queryset.filter(filtros)

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_summary="Buscar SKUs",
    tags=["inventario-sku"],
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description='Búsqueda libre por nombre, código SKU o código de barras', type=openapi.TYPE_STRING),
        openapi.Parameter('nombre', openapi.IN_QUERY, description='Filtrar por nombre (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('sku_codigo', openapi.IN_QUERY, description='Filtrar por código de SKU (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_barras', openapi.IN_QUERY, description='Filtrar por código de barras (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def buscar_skus(request):
    """
    Busca SKUs por nombre, código SKU o código de barras. Respuesta paginada.
    """
    queryset = InventarioSKU.objects.filter(is_active=True).order_by('nombre')

    q = request.query_params.get('q')
    nombre = request.query_params.get('nombre')
    sku_codigo = request.query_params.get('sku_codigo')
    codigo_barras = request.query_params.get('codigo_barras')

    filtros = Q()
    if q:
        ql = q.strip()
        if ql:
            filtros |= Q(nombre__icontains=ql)
            filtros |= Q(codigo_sku__icontains=ql)
            filtros |= Q(barcode__icontains=ql)
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if sku_codigo:
        filtros &= Q(codigo_sku__icontains=sku_codigo)
    if codigo_barras:
        filtros &= Q(barcode__icontains=codigo_barras)

    if filtros:
        queryset = queryset.filter(filtros)

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='get', operation_summary="Detalle de SKU con bodegas", tags=["inventario-sku"])
@api_view(['GET'])
def detalle_sku_con_bodegas(request, pk):
    """
    Detalle de un SKU específico incluyendo sus bodegas.
    """
    try:
        sku = InventarioSKU.objects.prefetch_related('bodegas').get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({'error': 'SKU no encontrado'}, status=404)

    serializer = InventarioSKUSerializer(sku)
    return Response(serializer.data)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('clasificacion', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Filtrar por clasificación (consignacion/controlado)")
], operation_summary="Listar SKUs filtrados por clasificación", tags=["inventario-sku"])
@api_view(['GET'])
def listar_skus_filtrados(request):
    """
    Lista SKUs filtrados por clasificación: 'consignacion' o 'controlado'.
    """
    clasificacion = request.GET.get('clasificacion')
    if clasificacion not in ['consignacion', 'controlado']:
        return Response({'error': 'Clasificación inválida'}, status=400)

    skus = InventarioSKU.objects.filter(is_active=True, clasificacion_producto=clasificacion).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(skus, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='get', operation_summary="Listar SKUs (sin paginación, solo id/nombre/código)", tags=["inventario-sku"])
@api_view(['GET'])
def sku_listar_completo(request):
    """
    Lista simplificada de SKUs (id, nombre, código_sku) sin paginación.
    """
    skus = InventarioSKU.objects.filter(is_active=True).order_by('nombre').only('id', 'codigo_sku', 'nombre')
    data = [{"id": sku.id, "codigo_sku": sku.codigo_sku, "nombre": sku.nombre} for sku in skus]
    return Response({"results": data})
