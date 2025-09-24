import io
import re
import unicodedata
import zipfile
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from xml.etree import ElementTree as ET

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from api.utils.pagination import CustomPageNumberPagination
from ..models.cargaMasivaModel import (
    CargaMasivaExistencia,
    CargaMasivaExistenciaItem,
    CargaMasivaPrecio,
    CargaMasivaPrecioItem,
)
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU
from ..models.inventarioPrecioSkuModel import PrecioSKU
from ..serializers.cargaMasivaSerializer import (
    CargaMasivaExistenciaSerializer,
    CargaMasivaPrecioSerializer,
)


def _resolve_username(request):
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        return user.username
    return request.headers.get('X-User') or None


def _column_index(col_letters: str) -> int:
    result = 0
    for ch in col_letters.upper():
        if 'A' <= ch <= 'Z':
            result = result * 26 + (ord(ch) - ord('A') + 1)
    return max(result - 1, 0)


def _normalize_header_value(value) -> str:
    text = str(value or '').strip().lower()
    if not text:
        return ''
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(ch for ch in normalized if not unicodedata.combining(ch))


def _header_token(value) -> str:
    normalized = _normalize_header_value(value)
    return re.sub(r'[^a-z0-9]', '', normalized)


def _load_excel_rows(file_obj):
    try:
        file_obj.seek(0)
    except Exception:
        pass

    data = file_obj.read()
    if not data:
        return []

    try:
        zip_buffer = io.BytesIO(data)
        workbook = zipfile.ZipFile(zip_buffer)
    finally:
        try:
            file_obj.seek(0)
        except Exception:
            pass

    ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    shared_strings = []
    if 'xl/sharedStrings.xml' in workbook.namelist():
        ss_tree = ET.fromstring(workbook.read('xl/sharedStrings.xml'))
        for si in ss_tree.findall('main:si', ns):
            text_parts = [t.text or '' for t in si.findall('.//main:t', ns)]
            shared_strings.append(''.join(text_parts))

    sheet_name = 'xl/worksheets/sheet1.xml'
    if sheet_name not in workbook.namelist():
        candidates = [name for name in workbook.namelist() if name.startswith('xl/worksheets/sheet')]
        if not candidates:
            return []
        sheet_name = candidates[0]

    sheet_tree = ET.fromstring(workbook.read(sheet_name))
    rows = []

    for row in sheet_tree.findall('.//main:row', ns):
        row_map = {}
        max_index = 0
        for cell in row.findall('main:c', ns):
            ref = cell.attrib.get('r', 'A1')
            col_letters = re.sub(r'[^A-Z]', '', ref.upper()) or 'A'
            col_index = _column_index(col_letters)
            max_index = max(max_index, col_index)

            cell_type = cell.attrib.get('t')
            value_node = cell.find('main:v', ns)
            value = ''
            if cell_type == 's':
                if value_node is not None and value_node.text is not None:
                    idx = int(value_node.text)
                    if 0 <= idx < len(shared_strings):
                        value = shared_strings[idx]
            else:
                if value_node is not None and value_node.text is not None:
                    value = value_node.text

            row_map[col_index] = value

        if row_map:
            row_values = [row_map.get(i, '') for i in range(max_index + 1)]
        else:
            row_values = ['']
        rows.append(row_values)

    return rows


def _validate_skus(codes):
    existing = set(
        InventarioSKU.objects.filter(codigo_sku__in=codes)
        .values_list('codigo_sku', flat=True)
    )
    missing = [code for code in codes if code not in existing]
    return missing


@api_view(['GET'])
def listar_cargas_existencias(request):
    qs = CargaMasivaExistencia.objects.all().order_by('-created_at')
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = CargaMasivaExistenciaSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def detalle_carga_existencias(request, pk):
    try:
        carga = CargaMasivaExistencia.objects.get(pk=pk)
    except CargaMasivaExistencia.DoesNotExist:
        return Response({'error': 'Carga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CargaMasivaExistenciaSerializer(carga)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def crear_carga_existencias(request):
    bodega = request.data.get('bodega')
    archivo = request.FILES.get('archivo')

    if not bodega:
        return Response({'error': 'Debe seleccionar una bodega'}, status=status.HTTP_400_BAD_REQUEST)
    if not archivo:
        return Response({'error': 'Debe adjuntar un archivo de Excel (.xlsx)'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rows = _load_excel_rows(archivo)
    except Exception as exc:
        return Response({'error': f'No fue posible leer el archivo: {exc}'}, status=status.HTTP_400_BAD_REQUEST)

    if len(rows) <= 1:
        return Response({'error': 'El archivo no contiene registros para procesar'}, status=status.HTTP_400_BAD_REQUEST)

    header_tokens = [_header_token(cell) for cell in rows[0]] if rows else []
    sku_aliases = {'sku', 'codigosku', 'codigo'}
    cantidad_aliases = {
        'cantidad',
        'cantidadtotal',
        'cantidaddisponible',
        'cantidades',
        'existencia',
        'existencias',
        'qty',
        'cantidadfinal',
    }

    sku_idx = next((i for i, token in enumerate(header_tokens) if token in sku_aliases), None)
    cantidad_idx = next((i for i, token in enumerate(header_tokens) if token in cantidad_aliases), None)

    if sku_idx is None:
        sku_idx = 0
    if cantidad_idx is None:
        cantidad_idx = 1

    acumulado = defaultdict(int)
    for idx, row in enumerate(rows[1:], start=2):
        row = list(row)
        sku_raw = row[sku_idx] if sku_idx < len(row) else ''
        cantidad_raw = row[cantidad_idx] if cantidad_idx < len(row) else ''
        sku_code = str(sku_raw).strip() if sku_raw else ''
        if not sku_code:
            continue
        try:
            cantidad_dec = Decimal(str(cantidad_raw or 0))
            if cantidad_dec < 0:
                return Response({'error': f'La cantidad no puede ser negativa (fila {idx}, SKU {sku_code})'}, status=status.HTTP_400_BAD_REQUEST)
            cantidad = int(cantidad_dec.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        except Exception:
            return Response({'error': f'Cantidad inválida en la fila {idx} para el SKU {sku_code}'}, status=status.HTTP_400_BAD_REQUEST)
        if cantidad == 0:
            continue
        acumulado[sku_code] += cantidad

    if not acumulado:
        return Response({'error': 'No hay cantidades válidas para cargar'}, status=status.HTTP_400_BAD_REQUEST)

    missing = _validate_skus(list(acumulado.keys()))
    if missing:
        return Response({'error': 'Existen SKU que no están registrados', 'skus': missing}, status=status.HTTP_400_BAD_REQUEST)

    username = _resolve_username(request)
    carga = CargaMasivaExistencia.objects.create(
        bodega=bodega,
        usuario=username,
        archivo_nombre=getattr(archivo, 'name', None),
    )

    sku_objs = {s.codigo_sku: s for s in InventarioSKU.objects.filter(codigo_sku__in=acumulado.keys())}

    for sku_code, cantidad in acumulado.items():
        sku_obj = sku_objs.get(sku_code)
        bodega_sku, _ = BodegaSKU.objects.select_for_update().get_or_create(
            sku=sku_obj,
            nombre_bodega=bodega,
            defaults={'cantidad': 0},
        )
        cantidad_anterior = int(bodega_sku.cantidad or 0)
        bodega_sku.cantidad = cantidad_anterior + int(cantidad)
        bodega_sku.save()

        CargaMasivaExistenciaItem.objects.create(
            carga=carga,
            sku=sku_code,
            descripcion=sku_obj.nombre,
            cantidad_cargada=int(cantidad),
            cantidad_anterior=cantidad_anterior,
            cantidad_resultante=int(bodega_sku.cantidad),
        )

    serializer = CargaMasivaExistenciaSerializer(carga)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def listar_cargas_precios(request):
    qs = CargaMasivaPrecio.objects.all().order_by('-created_at')
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = CargaMasivaPrecioSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def detalle_carga_precios(request, pk):
    try:
        carga = CargaMasivaPrecio.objects.get(pk=pk)
    except CargaMasivaPrecio.DoesNotExist:
        return Response({'error': 'Carga no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CargaMasivaPrecioSerializer(carga)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def crear_carga_precios(request):
    seguro = request.data.get('seguro')
    archivo = request.FILES.get('archivo')

    if not seguro:
        return Response({'error': 'Debe seleccionar un seguro'}, status=status.HTTP_400_BAD_REQUEST)
    if not archivo:
        return Response({'error': 'Debe adjuntar un archivo de Excel (.xlsx)'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rows = _load_excel_rows(archivo)
    except Exception as exc:
        return Response({'error': f'No fue posible leer el archivo: {exc}'}, status=status.HTTP_400_BAD_REQUEST)

    if len(rows) <= 1:
        return Response({'error': 'El archivo no contiene registros para procesar'}, status=status.HTTP_400_BAD_REQUEST)

    novedades = {}
    for idx, row in enumerate(rows[1:], start=2):
        row = list(row)
        if len(row) < 2:
            row += [None] * (2 - len(row))
        sku_raw, precio_raw = row[:2]
        sku_code = str(sku_raw).strip() if sku_raw else ''
        if not sku_code:
            continue
        try:
            precio = Decimal(str(precio_raw)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except Exception:
            return Response({'error': f'Precio inválido en la fila {idx} para el SKU {sku_code}'}, status=status.HTTP_400_BAD_REQUEST)
        if precio < 0:
            return Response({'error': f'El precio no puede ser negativo (fila {idx}, SKU {sku_code})'}, status=status.HTTP_400_BAD_REQUEST)
        novedades[sku_code] = precio

    if not novedades:
        return Response({'error': 'No hay precios válidos para procesar'}, status=status.HTTP_400_BAD_REQUEST)

    missing = _validate_skus(list(novedades.keys()))
    if missing:
        return Response({'error': 'Existen SKU que no están registrados', 'skus': missing}, status=status.HTTP_400_BAD_REQUEST)

    username = _resolve_username(request)
    carga = CargaMasivaPrecio.objects.create(
        seguro=seguro,
        usuario=username,
        archivo_nombre=getattr(archivo, 'name', None),
    )

    sku_objs = {s.codigo_sku: s for s in InventarioSKU.objects.filter(codigo_sku__in=novedades.keys())}

    for sku_code, precio in novedades.items():
        sku_obj = sku_objs.get(sku_code)
        precio_qs = PrecioSKU.objects.select_for_update().filter(
            sku=sku_obj,
            seguro_nombre__iexact=seguro,
            is_active=True,
        ).order_by('-vigente_desde')
        precio_prev = precio_qs.first()
        if precio_prev:
            precio_anterior = precio_prev.precio
            precio_prev.precio = precio
            precio_prev.sku_nombre = sku_obj.nombre
            precio_prev.save(update_fields=['precio', 'sku_nombre'])
            precio_final = precio_prev.precio
        else:
            precio_prev = PrecioSKU.objects.create(
                sku=sku_obj,
                sku_nombre=sku_obj.nombre,
                seguro_nombre=seguro,
                precio=precio,
            )
            precio_anterior = Decimal('0.00')
            precio_final = precio_prev.precio

        CargaMasivaPrecioItem.objects.create(
            carga=carga,
            sku=sku_code,
            descripcion=sku_obj.nombre,
            precio_anterior=precio_anterior,
            precio_nuevo=precio_final,
        )

    serializer = CargaMasivaPrecioSerializer(carga)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
