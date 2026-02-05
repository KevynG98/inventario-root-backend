from decimal import Decimal, InvalidOperation
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from openpyxl import load_workbook

from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioProductoModel import InventarioProducto
from ..serializers.inventarioProductoSerializer import InventarioProductoSerializer


def _parse_decimal(value, default="0"):
    """
    Convierte valores de Excel a Decimal de forma tolerante.
    """
    if value is None:
        return Decimal(default)
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    text = str(value).strip().replace(",", "")
    if not text:
        return Decimal(default)
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _codigo_generado(existentes, contador):
    """
    Genera un código con prefijo IMP- que no exista en la base/local.
    """
    while True:
        codigo = f"IMP-{contador:05d}"
        contador += 1
        if codigo not in existentes:
            existentes.add(codigo)
            return codigo, contador


@swagger_auto_schema(
    method='get', 
    operation_summary="Listar productos activos con filtros", 
    tags=["inventario-productos"],
    manual_parameters=[
        openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Filtrar por nombre"),
        openapi.Parameter('min_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Precio mínimo"),
        openapi.Parameter('max_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Precio máximo"),
    ]
)
@api_view(['GET'])
def listar_productos(request):
    inventarios = InventarioProducto.objects.filter(is_active=True).order_by('id')

    # Filtros
    nombre = request.query_params.get('nombre')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if nombre:
        inventarios = inventarios.filter(nombre__icontains=nombre)
    if min_price:
        try:
            inventarios = inventarios.filter(precio_stock__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            inventarios = inventarios.filter(precio_stock__lte=max_price)
        except ValueError:
            pass

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(inventarios, request)
    serializer = InventarioProductoSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(method='post', request_body=InventarioProductoSerializer, operation_summary="Crear nuevo producto", tags=["inventario-productos"])
@api_view(['POST'])
def crear_producto(request):
    serializer = InventarioProductoSerializer(data=request.data, context={'request': request})
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
    serializer = InventarioProductoSerializer(inventario, context={'request': request})
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=InventarioProductoSerializer, operation_summary="Actualizar producto", tags=["inventario-productos"])
@api_view(['PUT'])
def actualizar_producto(request, pk):
    try:
        inventario = InventarioProducto.objects.get(pk=pk)
    except InventarioProducto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventarioProductoSerializer(inventario, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("❌ Error al actualizar producto:", serializer.errors)
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
        openapi.Parameter('q', openapi.IN_QUERY, description='Búsqueda libre por nombre o código de inventario', type=openapi.TYPE_STRING),
        openapi.Parameter('nombre', openapi.IN_QUERY, description='Filtrar por nombre (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_inventario', openapi.IN_QUERY, description='Filtrar por código de inventario (icontains)', type=openapi.TYPE_STRING),
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

    filtros = Q()
    if q:
        ql = q.strip()
        if ql:
            filtros |= Q(nombre__icontains=ql)
            filtros |= Q(codigo_inventario__icontains=ql)
    if nombre:
        filtros &= Q(nombre__icontains=nombre)
    if codigo_inventario:
        filtros &= Q(codigo_inventario__icontains=codigo_inventario)

    if filtros:
        queryset = queryset.filter(filtros)

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioProductoSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_summary="Carga masiva de productos desde Excel (xlsx)",
    tags=["inventario-productos"],
    manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_FORM,
            description='Archivo Excel con columnas: Nombre, Precio de venta, Coste',
            type=openapi.TYPE_FILE,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Resultado de la importación",
            examples={
                "application/json": {
                    "creados": 10,
                    "errores": [
                        {"fila": 3, "detalle": "Nombre vacío"}
                    ],
                    "resumen": "10 productos creados, 2 filas con errores"
                }
            }
        )
    }
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def carga_masiva_productos(request):
    """
    Recibe un Excel y crea productos en bloque con valores por defecto.
    Columnas soportadas: Nombre, Precio de venta, Coste.
    """
    archivo = request.FILES.get('file')
    if not archivo:
        return Response({"error": "No se envió archivo con clave 'file'."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        libro = load_workbook(archivo, data_only=True, read_only=True)
        hoja = libro.active
    except Exception as exc:
        return Response({"error": "No se pudo leer el Excel", "detalle": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    existentes = set(InventarioProducto.objects.values_list('codigo_inventario', flat=True))
    contador = len(existentes) + 1

    creados = []
    errores = []
    objetos = []
    batch_size = 500

    for idx, fila in enumerate(hoja.iter_rows(min_row=2, values_only=True), start=2):
        nombre, precio_venta, coste = (fila + (None, None, None))[:3] if fila else (None, None, None)
        if not nombre or str(nombre).strip() == "":
            errores.append({"fila": idx, "detalle": "Nombre vacío"})
            continue

        codigo, contador = _codigo_generado(existentes, contador)
        payload = {
            "nombre": str(nombre).strip(),
            "codigo_inventario": codigo,
            "precio_compre": _parse_decimal(coste),
            "precio_stock": _parse_decimal(precio_venta),
            "is_active": True,
        }

        serializer = InventarioProductoSerializer(data=payload)
        if serializer.is_valid():
            objetos.append(InventarioProducto(**serializer.validated_data))
        else:
            errores.append({"fila": idx, "detalle": serializer.errors})

        # flush por lotes para no agotar memoria
        if len(objetos) >= batch_size:
            InventarioProducto.objects.bulk_create(objetos, batch_size=batch_size)
            creados.extend([obj.codigo_inventario for obj in objetos])
            objetos = []

    if objetos:
        InventarioProducto.objects.bulk_create(objetos, batch_size=batch_size)
        creados.extend([obj.codigo_inventario for obj in objetos])

    resumen = f"{len(creados)} productos creados, {len(errores)} filas con errores"
    return Response(
        {
            "creados": len(creados),
            "codigos_generados": creados[:50],  # muestra primeros 50
            "errores": errores,
            "resumen": resumen,
        },
        status=status.HTTP_200_OK
    )
