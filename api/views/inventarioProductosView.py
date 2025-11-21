from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioProductoModel import InventarioProducto
from ..serializers.inventarioProductoSerializer import InventarioProductoSerializer


@swagger_auto_schema(method='get', operation_summary="Listar productos activos", tags=["inventario-productos"])
@api_view(['GET'])
def listar_productos(request):
    inventarios = InventarioProducto.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(inventarios, request)
    serializer = InventarioProductoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', request_body=InventarioProductoSerializer, operation_summary="Crear nuevo producto", tags=["inventario-productos"])
@api_view(['POST'])
def crear_producto(request):
    serializer = InventarioProductoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='get', operation_summary="Obtener producto por ID", tags=["inventario-productos"])
@api_view(['GET'])
def obtener_producto(request, pk):
    try:
        inventario = InventarioProducto.objects.get(pk=pk)
    except InventarioProducto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioProductoSerializer(inventario)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=InventarioProductoSerializer, operation_summary="Actualizar producto", tags=["inventario-productos"])
@api_view(['PUT'])
def actualizar_producto(request, pk):
    try:
        inventario = InventarioProducto.objects.get(pk=pk)
    except InventarioProducto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventarioProductoSerializer(inventario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', operation_summary="Eliminar producto (soft delete)", tags=["inventario-productos"])
@api_view(['DELETE'])
def eliminar_producto(request, pk):
    try:
        inventario = InventarioProducto.objects.get(pk=pk)
    except InventarioProducto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    inventario.is_active = False
    inventario.save(update_fields=['is_active'])
    return Response({"mensaje": "Producto desactivado (soft delete)"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="Buscar productos",
    tags=["inventario-productos"],
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description='Búsqueda libre por nombre, código de inventario o código de barras', type=openapi.TYPE_STRING),
        openapi.Parameter('nombre', openapi.IN_QUERY, description='Filtrar por nombre (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_inventario', openapi.IN_QUERY, description='Filtrar por código de inventario (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_barras', openapi.IN_QUERY, description='Filtrar por código de barras (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def buscar_productos(request):
    queryset = InventarioProducto.objects.filter(is_active=True).order_by('nombre')

    q = request.query_params.get('q')
    nombre = request.query_params.get('nombre')
    codigo_inventario = request.query_params.get('codigo_inventario')
    codigo_barras = request.query_params.get('codigo_barras')

    filtros = Q()
    if q:
        ql = q.strip()
        if ql:
            filtros |= Q(nombre__icontains=ql)
            filtros |= Q(codigo_inventario__icontains=ql)
            filtros |= Q(barcode__icontains=ql)
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if codigo_inventario:
        filtros &= Q(codigo_inventario__icontains=codigo_inventario)
    if codigo_barras:
        filtros &= Q(barcode__icontains=codigo_barras)

    if filtros:
        queryset = queryset.filter(filtros)

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioProductoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
