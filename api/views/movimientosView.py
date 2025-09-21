# views/movimientosView.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.movimientoHistoricoModel import MovimientoHistorico
from ..serializers.MovimientoHistoricoSerializer import MovimientoHistoricoSerializer
from django.db.models import Q
from ..models.inventariosSkuModel import InventarioSKU
from ..models.entradasModel import Entrada, EntradaItem
from ..models.salidasModel import Salida, SalidaItem
from ..models.trasladosModel import Traslado, TrasladoItem
from ..models.cargaMasivaModel import CargaMasivaExistenciaItem
from datetime import datetime
from django.utils import timezone

@api_view(['GET'])
def listar_historial_movimientos(request):
    queryset = MovimientoHistorico.objects.all()
    sku = request.GET.get('sku')
    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')

    if sku:
        queryset = queryset.filter(sku__codigo_sku=sku)
    if inicio and fin:
        queryset = queryset.filter(fecha__range=[inicio, fin])

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(queryset.order_by('-fecha'), request)
    serializer = MovimientoHistoricoSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def listar_movimientos_detalle(request):
    """
    Lista movimientos transaccionales por SKU con detalle unificado de Entradas, Salidas y Traslados.
    Filtros opcionales: bodega, categoria (nombre), subcategoria (nombre), sku (codigo_sku), inicio (YYYY-MM-DD), fin (YYYY-MM-DD)
    """
    bodega = request.GET.get('bodega')
    categoria = request.GET.get('categoria')
    subcategoria = request.GET.get('subcategoria')
    sku_code = request.GET.get('sku')
    inicio = request.GET.get('inicio')
    fin = request.GET.get('fin')

    def parse_dt(d):
        try:
            return datetime.strptime(d, '%Y-%m-%d')
        except Exception:
            return None

    dt_inicio = parse_dt(inicio) if inicio else None
    dt_fin = parse_dt(fin) if fin else None

    # Helper to filter by sku category/subcategory
    def sku_match(code):
        try:
            sku = InventarioSKU.objects.filter(codigo_sku=code).first()
            if not sku:
                return False
            if categoria and (sku.categoria or '').lower() != categoria.lower():
                return False
            if subcategoria and ((sku.subcategoria or '').lower() != subcategoria.lower()):
                return False
            return True
        except Exception:
            return False

    items = []
    # Entradas
    q_e = Entrada.objects.all()
    if bodega:
        q_e = q_e.filter(bodega__icontains=bodega)
    if dt_inicio:
        q_e = q_e.filter(created_at__date__gte=dt_inicio.date())
    if dt_fin:
        q_e = q_e.filter(created_at__date__lte=dt_fin.date())
    for e in q_e:
        for it in e.items.all():
            if sku_code and it.sku != sku_code:
                continue
            if not sku_match(it.sku):
                continue
            tipo = e.tipo_entrada.replace('_', ' ').title() if e.tipo_entrada else 'Entrada'
            dt = e.created_at
            if dt:
                try:
                    dt = timezone.localtime(dt)
                except Exception:
                    pass
            items.append({
                'fecha_hora': dt.strftime('%Y-%m-%d %H:%M:%S') if dt else '',
                'sku': it.sku,
                'nombre': InventarioSKU.objects.filter(codigo_sku=it.sku).values_list('nombre', flat=True).first() or '',
                'movimiento': f"Entrada-{tipo}",
                'cantidad': float(it.cantidad),
            })

    # Salidas
    q_s = Salida.objects.all()
    if bodega:
        q_s = q_s.filter(bodega__icontains=bodega)
    if dt_inicio:
        q_s = q_s.filter(created_at__date__gte=dt_inicio.date())
    if dt_fin:
        q_s = q_s.filter(created_at__date__lte=dt_fin.date())
    for s in q_s:
        for it in s.items.all():
            if sku_code and it.sku != sku_code:
                continue
            if not sku_match(it.sku):
                continue
            tipo = s.tipo_salida.replace('_', ' ').title() if s.tipo_salida else 'Salida'
            dt = s.created_at
            if dt:
                try:
                    dt = timezone.localtime(dt)
                except Exception:
                    pass
            items.append({
                'fecha_hora': dt.strftime('%Y-%m-%d %H:%M:%S') if dt else '',
                'sku': it.sku,
                'nombre': InventarioSKU.objects.filter(codigo_sku=it.sku).values_list('nombre', flat=True).first() or '',
                'movimiento': f"Salida-{tipo}",
                'cantidad': -float(it.cantidad),
            })

    # Traslados
    # Traslados: excluir ANULADO para que no afecten el histórico acumulado
    q_t = Traslado.objects.exclude(estatus='ANULADO')
    if dt_inicio:
        q_t = q_t.filter(fecha_envio__date__gte=dt_inicio.date())
    if dt_fin:
        q_t = q_t.filter(fecha_envio__date__lte=dt_fin.date())
    for t in q_t:
        for it in t.items.all():
            if sku_code and it.sku != sku_code:
                continue
            if not sku_match(it.sku):
                continue
            # Salida desde origen
            if (not bodega) or (t.bodega_origen and bodega.lower() in t.bodega_origen.lower()):
                dt = t.fecha_envio
                if dt:
                    try:
                        dt = timezone.localtime(dt)
                    except Exception:
                        pass
                items.append({
                    'fecha_hora': dt.strftime('%Y-%m-%d %H:%M:%S') if dt else '',
                    'sku': it.sku,
                    'nombre': InventarioSKU.objects.filter(codigo_sku=it.sku).values_list('nombre', flat=True).first() or '',
                    'movimiento': f"Traslado-{t.bodega_destino}",
                    'cantidad': -float(it.cantidad),
                })
            # Entrada al destino (solo si fue recibido)
            if t.estatus == 'RECIBIDO' and ((not bodega) or (t.bodega_destino and bodega.lower() in t.bodega_destino.lower())):
                dt2 = t.fecha_recibido
                if dt2:
                    try:
                        dt2 = timezone.localtime(dt2)
                    except Exception:
                        pass
                items.append({
                    'fecha_hora': dt2.strftime('%Y-%m-%d %H:%M:%S') if dt2 else '',
                    'sku': it.sku,
                    'nombre': InventarioSKU.objects.filter(codigo_sku=it.sku).values_list('nombre', flat=True).first() or '',
                    'movimiento': f"Traslado-{t.bodega_origen}",
                    'cantidad': float(it.cantidad),
                })

    # Cargas masivas (existencias)
    q_c = CargaMasivaExistenciaItem.objects.select_related('carga')
    if bodega:
        q_c = q_c.filter(carga__bodega__icontains=bodega)
    if dt_inicio:
        q_c = q_c.filter(carga__created_at__date__gte=dt_inicio.date())
    if dt_fin:
        q_c = q_c.filter(carga__created_at__date__lte=dt_fin.date())

    for carga_item in q_c:
        if sku_code and carga_item.sku != sku_code:
            continue
        if not sku_match(carga_item.sku):
            continue
        dt = carga_item.carga.created_at
        if dt:
            try:
                dt = timezone.localtime(dt)
            except Exception:
                pass
        items.append({
            'fecha_hora': dt.strftime('%Y-%m-%d %H:%M:%S') if dt else '',
            'sku': carga_item.sku,
            'nombre': InventarioSKU.objects.filter(codigo_sku=carga_item.sku).values_list('nombre', flat=True).first() or '',
            'movimiento': 'Carga-Masiva',
            'cantidad': float(carga_item.cantidad_cargada),
        })

    # Ordenar por fecha y calcular inventario acumulado
    def key_sort(x):
        try:
            return datetime.strptime(x['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min
    items.sort(key=key_sort)

    inventario = 0.0
    for it in items:
        inventario += float(it['cantidad'])
        it['inventario'] = inventario

    # Paginación simple en memoria
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(items, request)
    return paginator.get_paginated_response(page)
