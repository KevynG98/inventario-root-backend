from functools import reduce
import operator as op

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


# -----------------------------
# Helpers para detección segura
# -----------------------------
def _detect_sku_fields():
    """
    Detecta en tiempo de ejecución cómo se llaman en InventarioSKU:
    - el código del SKU (p.ej. 'codigo_sku', 'codigo', 'sku_codigo', etc.)
    - el código de barras (p.ej. 'codigo_barras', 'barcode', 'ean', etc.)
    - algún campo de texto útil para búsqueda libre (p.ej. 'nombre', 'descripcion_estado_cuenta')
    """
    sku_fk = PrecioSKU._meta.get_field('sku')  # si tu FK NO se llama 'sku', ajusta aquí
    sku_model = sku_fk.remote_field.model
    field_names = {f.name for f in sku_model._meta.fields}

    candidates_code = ['codigo_sku', 'codigo', 'sku_codigo', 'code', 'sku']
    candidates_barcode = ['codigo_barras', 'codigo_barra', 'barcode', 'ean', 'ean13', 'upc', 'gtin', 'bar_code']
    candidates_text = ['nombre', 'descripcion_estado_cuenta', 'descripcion', 'titulo', 'name']

    code_field = next((n for n in candidates_code if n in field_names), None)
    barcode_field = next((n for n in candidates_barcode if n in field_names), None)
    text_field = next((n for n in candidates_text if n in field_names), None)

    return code_field, barcode_field, text_field


@swagger_auto_schema(
    method='get',
    operation_summary="Buscar precios con filtros",
    tags=["inventario-precio"],
    manual_parameters=[
        openapi.Parameter('is_active', openapi.IN_QUERY, description='Filtrar por is_active (true/false). Default: true', type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('sku_id', openapi.IN_QUERY, description='ID del SKU (exacto)', type=openapi.TYPE_INTEGER),
        openapi.Parameter('sku_codigo', openapi.IN_QUERY, description='Código del SKU (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('codigo_barras', openapi.IN_QUERY, description='Código de barras (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('seguro_nombre', openapi.IN_QUERY, description='Nombre del seguro (icontains)', type=openapi.TYPE_STRING),
        openapi.Parameter('precio_min', openapi.IN_QUERY, description='Precio mínimo (>=)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('precio_max', openapi.IN_QUERY, description='Precio máximo (<=)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('q', openapi.IN_QUERY, description='Búsqueda libre (seguro + campos detectados del SKU)', type=openapi.TYPE_STRING),
        openapi.Parameter('ordering', openapi.IN_QUERY, description='Orden: "precio", "-precio", "id", "-id"', type=openapi.TYPE_STRING),
        openapi.Parameter('limit', openapi.IN_QUERY, description='Límite de resultados (default 100)', type=openapi.TYPE_INTEGER),
        openapi.Parameter('offset', openapi.IN_QUERY, description='Desplazamiento para paginación (default 0)', type=openapi.TYPE_INTEGER),
    ],
)
@api_view(['GET'])
def buscar_precios(request):
    """
    Busca precios aplicando filtros por query params.
    - Por defecto devuelve sólo is_active=True (cámbialo con ?is_active=false)
    - Soporta búsqueda libre con ?q=
    - Paginación simple con limit/offset y orden con ?ordering=
    - No revienta si el modelo InventarioSKU no tiene 'codigo_barras' u otros campos: detecta primero.
    """
    qs = PrecioSKU.objects.select_related('sku').all()

    # is_active por defecto en True
    is_active_param = request.query_params.get('is_active')
    if is_active_param is None:
        qs = qs.filter(is_active=True)
    else:
        val = str(is_active_param).lower()
        if val in ('true', '1', 't', 'yes', 'y'):
            qs = qs.filter(is_active=True)
        elif val in ('false', '0', 'f', 'no', 'n'):
            qs = qs.filter(is_active=False)

    # Detectar campos reales del modelo InventarioSKU
    code_field, barcode_field, text_field = _detect_sku_fields()
    # print("SKU fields:", code_field, barcode_field, text_field)  # útil para debug local

    # Filtros específicos
    sku_id = request.query_params.get('sku_id')
    if sku_id:
        qs = qs.filter(sku_id=sku_id)

    sku_codigo = request.query_params.get('sku_codigo')
    if sku_codigo and code_field:
        qs = qs.filter(**{f"sku__{code_field}__icontains": sku_codigo})

    codigo_barras = request.query_params.get('codigo_barras')
    if codigo_barras and barcode_field:
        qs = qs.filter(**{f"sku__{barcode_field}__icontains": codigo_barras})

    seguro_nombre = request.query_params.get('seguro_nombre')
    if seguro_nombre:
        qs = qs.filter(seguro_nombre__icontains=seguro_nombre)

    precio_min = request.query_params.get('precio_min')
    if precio_min is not None:
        qs = qs.filter(precio__gte=precio_min)

    precio_max = request.query_params.get('precio_max')
    if precio_max is not None:
        qs = qs.filter(precio__lte=precio_max)

    # Búsqueda libre
    q = request.query_params.get('q')
    if q:
        condiciones = [Q(seguro_nombre__icontains=q)]
        if code_field:
            condiciones.append(Q(**{f"sku__{code_field}__icontains": q}))
        if barcode_field:
            condiciones.append(Q(**{f"sku__{barcode_field}__icontains": q}))
        if text_field:
            condiciones.append(Q(**{f"sku__{text_field}__icontains": q}))
        qs = qs.filter(reduce(op.or_, condiciones)).distinct()

    # Orden
    ordering = request.query_params.get('ordering', '-id')
    try:
        qs = qs.order_by(ordering)
    except Exception:
        qs = qs.order_by('-id')

    # Paginación simple limit/offset (si usas paginación DRF global, quita esto)
    try:
        limit = int(request.query_params.get('limit', 100))
        offset = int(request.query_params.get('offset', 0))
    except ValueError:
        return Response({'error': 'limit y offset deben ser enteros.'}, status=status.HTTP_400_BAD_REQUEST)

    total = qs.count()
    qs = qs[offset:offset + limit]

    serializer = PrecioSKUSerializer(qs, many=True)
    return Response({'count': total, 'results': serializer.data})
