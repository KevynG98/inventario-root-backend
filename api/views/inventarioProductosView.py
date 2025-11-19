from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventariosSkuModel import InventarioSKU
from ..serializers.inventarioSkuSerializer import InventarioSKUSerializer


@swagger_auto_schema(method='get', operation_summary="Listar productos activos", tags=["inventario-productos"])
@api_view(['GET'])
def listar_productos(request):
    skus = InventarioSKU.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(skus, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', request_body=InventarioSKUSerializer, operation_summary="Crear nuevo producto", tags=["inventario-productos"])
@api_view(['POST'])
def crear_producto(request):
    serializer = InventarioSKUSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='get', operation_summary="Obtener producto por ID", tags=["inventario-productos"])
@api_view(['GET'])
def obtener_producto(request, pk):
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioSKUSerializer(sku)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=InventarioSKUSerializer, operation_summary="Actualizar producto", tags=["inventario-productos"])
@api_view(['PUT'])
def actualizar_producto(request, pk):
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventarioSKUSerializer(sku, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', operation_summary="Eliminar producto (soft delete)", tags=["inventario-productos"])
@api_view(['DELETE'])
def eliminar_producto(request, pk):
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    sku.is_active = False
    sku.save(update_fields=['is_active'])
    return Response({"mensaje": "Producto desactivado (soft delete)"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="Buscar productos",
    tags=["inventario-productos"],
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
def buscar_productos(request):
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
