from datetime import datetime
from decimal import Decimal
import os

from django.db import transaction
from django.db import models
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models.requisisionesModel import Requisicion, ProductoRequisicion, ServicioRequisicion
from ..models.purchaseOrderModel import PurchaseOrder, PurchaseOrderDetail, PurchaseOrderLog
from ..models.inventariosSkuModel import InventarioSKU
from ..models.inventarioProveedoresModel import Proveedor
from ..serializers.purchaseOrderSerializer import PurchaseOrderSerializer
from api.utils.pagination import CustomPageNumberPagination
from ..serializers.purchaseOrderDetailSerializer import PurchaseOrderDetailSerializer


def _sum_requisicion_total(req: Requisicion) -> Decimal:
    total_prod = ProductoRequisicion.objects.filter(requisicion=req).aggregate(t=models.Sum('total'))['t'] or Decimal('0')
    total_serv = ServicioRequisicion.objects.filter(requisicion=req).aggregate(t=models.Sum('total'))['t'] or Decimal('0')
    return Decimal(total_prod) + Decimal(total_serv)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_requisiciones_autorizadas(request):
    estatus = request.GET.get('estatus')
    # Mapeo: AUTORIZADA -> 'aprobada' en el modelo actual
    estado = 'aprobada' if (estatus or '').upper() == 'AUTORIZADA' else None

    qs = Requisicion.objects.all()
    if estado:
        qs = qs.filter(estado=estado)

    data = []
    for r in qs.order_by('-created_at'):
        try:
            oc = PurchaseOrder.objects.filter(requisicion=r).order_by('-id').first()
        except Exception:
            oc = None
        numero = (oc.numero if oc and oc.numero else (str(oc.id) if oc else str(r.id)))
        solicitante_bodega = f"{(r.area_solicitante or '').strip()} - {(r.bodega or '').strip()}".strip(' -')
        tipo = (r.tipo_requisicion or '').strip().capitalize()  # Bien | Servicio
        total = _sum_requisicion_total(r)
        data.append({
            'id': r.id,
            'oc_id': oc.id if oc else None,
            'oc_estatus': oc.estatus if oc else None,
            'oc_numero': oc.numero if oc else None,
            'numero_orden_compra': numero,
            'fecha': (r.created_at.strftime('%Y-%m-%d') if r.created_at else None),
            'proveedor_nombre': '',  # No disponible en modelo actual
            'solicitante_bodega': solicitante_bodega,
            'tipo_requisicion': tipo or None,
            'total': str(total),
            'estatus': 'AUTORIZADA' if r.estado == 'aprobada' else r.estado.upper(),
        })
    return Response({'results': data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_oc_desde_requisicion(request, requisicion_id: int):
    req = get_object_or_404(Requisicion, id=requisicion_id)
    existing = PurchaseOrder.objects.filter(requisicion=req).order_by('-id').first()
    if existing:
        ser = PurchaseOrderSerializer(existing)
        return Response(ser.data, status=status.HTTP_200_OK)

    oc = PurchaseOrder.objects.create(
        requisicion=req,
        estatus='BORRADOR',
        proveedor_nombre=(req.proveedor or ''),
        solicitante_bodega=f"{(req.area_solicitante or '').strip()} - {(req.bodega or '').strip()}".strip(' -'),
        tipo_requisicion=(req.tipo_requisicion or '').strip().capitalize(),
        total=Decimal('0'),  # se recalcula abajo con IVA
    )

    # Clonar ítems desde requisición (productos/servicios)
    oc_total = Decimal('0')
    prod_qs = ProductoRequisicion.objects.filter(requisicion=req)
    for p in prod_qs:
        precio = Decimal(p.precio or 0)
        cantidad = Decimal(p.cantidad or 0)
        iva_unit = Decimal('0')
        try:
            sku = InventarioSKU.objects.filter(codigo_sku=p.sku).only('iva').first()
            if sku and (sku.iva or '').lower() == 'afecto':
                iva_unit = (precio * Decimal('0.12')).quantize(Decimal('0.01'))
        except Exception:
            pass
        total_item = (cantidad * (precio + iva_unit)).quantize(Decimal('0.01'))
        PurchaseOrderDetail.objects.create(
            orden=oc,
            codigo_sku=p.sku,
            descripcion=p.descripcion,
            unidad_medida=p.unidad,
            cantidad=cantidad,
            precio_sin_iva=precio,
            iva=iva_unit,
            total=total_item,
        )
        oc_total += total_item
    serv_qs = ServicioRequisicion.objects.filter(requisicion=req)
    for s in serv_qs:
        precio = Decimal(s.precio or 0)
        cantidad = Decimal(s.cantidad or 0)
        iva_unit = Decimal('0')  # servicios exentos por defecto (ajustable)
        total_item = (cantidad * (precio + iva_unit)).quantize(Decimal('0.01'))
        PurchaseOrderDetail.objects.create(
            orden=oc,
            codigo_sku='SERV',
            descripcion=s.descripcion,
            unidad_medida='SERV',
            cantidad=cantidad,
            precio_sin_iva=precio,
            iva=iva_unit,
            total=total_item,
        )
        oc_total += total_item

    oc.total = oc_total
    oc.save(update_fields=['total'])

    ser = PurchaseOrderSerializer(oc)
    return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_orden_compra(request, id: int):
    oc = get_object_or_404(PurchaseOrder, id=id)
    return Response(_oc_payload(oc))


def _oc_payload(oc: PurchaseOrder):
    items = PurchaseOrderDetail.objects.filter(orden=oc)
    data = PurchaseOrderSerializer(oc).data
    data['items'] = PurchaseOrderDetailSerializer(items, many=True).data

    # Añadir bitácora y campos de auditoría/visualización
    try:
        logs = list(PurchaseOrderLog.objects.filter(orden=oc).select_related('usuario').order_by('-timestamp'))
        data['bitacora'] = [{
            'accion': lg.accion,
            'usuario': getattr(lg.usuario, 'username', None),
            'observaciones': lg.observaciones,
            'timestamp': lg.timestamp.strftime('%Y-%m-%d %H:%M:%S') if lg.timestamp else None,
        } for lg in logs]
        gen = next((lg for lg in logs if lg.accion == 'GENERAR'), None)
        data['generada_por'] = getattr(gen.usuario, 'username', None) if gen else None
    except Exception:
        data['bitacora'] = []
        data['generada_por'] = None

    # Enlazar datos de la requisición para "visualizar"
    try:
        req = oc.requisicion
        data['requisicion_info'] = {
            'alta_por': req.usuario,
            'observaciones_alta': req.descripcion,
            'estado': req.estado,
            'estado_actualizado_por': req.estado_actualizado_por,
            'fecha': req.created_at.strftime('%Y-%m-%d %H:%M:%S') if req.created_at else None,
            'proveedor': req.proveedor,
            'centro_costo': req.centro_costo,
            'departamento': req.area_solicitante,
            'bodega': req.bodega,
            'tipo_requisicion': (req.tipo_requisicion or '').capitalize() if req.tipo_requisicion else None,
        }
    except Exception:
        data['requisicion_info'] = None

    return data


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_ordenes_compra(request):
    """
    Lista órdenes de compra con filtros simples.
    Query params:
      - estatus: valores UI {NUEVA, EDICION, ANULADA, AUTORIZADA}
      - page, page_size
    """
    estatus_ui = (request.GET.get('estatus') or '').strip().upper()
    mapping = {
        'NUEVA': 'BORRADOR',
        'EDICION': 'EDICION',
        'ANULADA': 'ANULADA',
        'AUTORIZADA': 'GENERADA',
    }
    qs = PurchaseOrder.objects.all().order_by('-id')
    if estatus_ui in mapping:
        qs = qs.filter(estatus=mapping[estatus_ui])

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(qs, request)
    data = []
    for oc in page:
        ui_status = {
            'BORRADOR': 'Nueva',
            'EDICION': 'Edición',
            'ANULADA': 'Anulada',
            'GENERADA': 'Autorizada',
        }.get(oc.estatus, oc.estatus)
        data.append({
            'id': oc.id,
            'numero': oc.numero or str(oc.id),
            'estatus': ui_status,
            'fecha': oc.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if oc.fecha_creacion else None,
            'proveedor': (oc.proveedor_nombre or oc.requisicion.proveedor or ''),
            'solicitante_bodega': oc.solicitante_bodega,
            'total': str(oc.total),
        })

    return paginator.get_paginated_response(data)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def editar_orden_compra(request, id: int):
    oc = get_object_or_404(PurchaseOrder, id=id)
    if oc.estatus not in {"BORRADOR", "EDICION"}:
        return Response({"detail": "Edición no permitida para este estatus."}, status=400)

    observaciones = (request.data or {}).get('observaciones')
    if not observaciones:
        return Response({"observaciones": ["Este campo es obligatorio."]}, status=400)

    # Campos simples
    for fld in ['fecha_entrega', 'condiciones_pago', 'dias_credito']:
        if fld in request.data:
            setattr(oc, fld, request.data.get(fld) or None)

    # CRUD items
    items_payload = request.data.get('items')
    if isinstance(items_payload, list):
        # Reemplazar items por simplicidad
        PurchaseOrderDetail.objects.filter(orden=oc).delete()
        total = Decimal('0')
        for it in items_payload:
            qty = Decimal(str(it.get('cantidad') or '0'))
            precio = Decimal(str(it.get('precio_sin_iva') or '0'))
            iva = Decimal(str(it.get('iva') or '0'))
            total_item = Decimal(str(it.get('total') or (qty * (precio + iva))))
            PurchaseOrderDetail.objects.create(
                orden=oc,
                codigo_sku=str(it.get('codigo_sku') or ''),
                descripcion=it.get('descripcion') or '',
                unidad_medida=it.get('unidad_medida') or '',
                cantidad=qty,
                precio_sin_iva=precio,
                iva=iva,
                total=total_item,
            )
            total += total_item
        oc.total = total

    oc.estatus = 'EDICION'
    oc.save()

    PurchaseOrderLog.objects.create(
        orden=oc,
        usuario=request.user if request.user and request.user.is_authenticated else None,
        accion='EDITAR',
        observaciones=observaciones,
    )

    return Response(_oc_payload(oc))


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def anular_orden_compra(request, id: int):
    oc = get_object_or_404(PurchaseOrder, id=id)
    observaciones = (request.data or {}).get('observaciones')
    if not observaciones:
        return Response({"observaciones": ["Este campo es obligatorio."]}, status=400)
    oc.estatus = 'ANULADA'
    oc.save(update_fields=['estatus'])
    PurchaseOrderLog.objects.create(
        orden=oc,
        usuario=request.user if request.user and request.user.is_authenticated else None,
        accion='ANULAR',
        observaciones=observaciones,
    )
    return Response(_oc_payload(oc))


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def generar_orden_compra(request, id: int):
    try:
        oc = get_object_or_404(PurchaseOrder, id=id)
        # Permitir que el cliente envíe campos de pago/fecha justo antes de generar
        data = request.data or {}
        fecha_entrega = data.get('fecha_entrega')
        condiciones_pago = data.get('condiciones_pago')
        dias_credito = data.get('dias_credito')

        # Actualizar campos si vienen en el request
        if fecha_entrega:
            try:
                from datetime import datetime as _dt
                oc.fecha_entrega = _dt.strptime(str(fecha_entrega), '%Y-%m-%d').date()
            except Exception:
                oc.fecha_entrega = None
        if condiciones_pago in (None, '', 'NULL'):
            oc.condiciones_pago = None
        elif condiciones_pago in ('CREDITO', 'CONTADO'):
            oc.condiciones_pago = condiciones_pago
        if oc.condiciones_pago == 'CREDITO':
            try:
                oc.dias_credito = int(dias_credito) if dias_credito is not None else oc.dias_credito
            except Exception:
                oc.dias_credito = None
        else:
            oc.dias_credito = None

        # Validaciones
        if not oc.condiciones_pago:
            return Response({"condiciones_pago": ["Defina las condiciones de pago."]}, status=400)
        if oc.condiciones_pago == 'CREDITO' and (oc.dias_credito not in {7, 15, 21, 30, 45, 60, 75, 90}):
            return Response({"dias_credito": ["Días de crédito inválidos."]}, status=400)
        items = list(PurchaseOrderDetail.objects.filter(orden=oc))
        if not items:
            return Response({"items": ["Debe agregar al menos 1 ítem válido."]}, status=400)
        for it in items:
            if it.cantidad <= 0 or (it.precio_sin_iva is None):
                return Response({"items": ["Ítems con cantidad/precio inválidos."]}, status=400)

        # Asignar número si hace falta y generar
        if not oc.numero:
            today = datetime.now().strftime('%Y%m%d')
            oc.numero = f"OC-{today}-{oc.id:05d}"
        oc.estatus = 'GENERADA'
        oc.save()

        PurchaseOrderLog.objects.create(
            orden=oc,
            usuario=request.user if request.user and request.user.is_authenticated else None,
            accion='GENERAR',
            observaciones=(request.data or {}).get('observaciones', 'Generación de orden de compra'),
        )
        return Response(_oc_payload(oc))
    except AssertionError as e:
        return Response({"detail": f"Error al generar OC: {e}"}, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def descargar_pdf_orden_compra(request, id: int):
    oc = get_object_or_404(PurchaseOrder, id=id)
    items = list(PurchaseOrderDetail.objects.filter(orden=oc))

    # Resolver datos de proveedor desde snapshot o catálogo
    # Tomar proveedor de la OC o, si no hay, de la requisición asociada
    proveedor_nombre_raw = (oc.proveedor_nombre or oc.requisicion.proveedor or '').strip()
    proveedor_obj = None
    if proveedor_nombre_raw:
        try:
            if proveedor_nombre_raw.isdigit():
                proveedor_obj = Proveedor.objects.filter(id=int(proveedor_nombre_raw)).first()
            if not proveedor_obj:
                proveedor_obj = Proveedor.objects.filter(nombre__iexact=proveedor_nombre_raw).first()
        except Exception:
            proveedor_obj = None

    proveedor_ctx = {
        "nombre": (proveedor_obj.nombre if proveedor_obj else proveedor_nombre_raw) or '',
        "direccion": (getattr(proveedor_obj, 'direccion', '') if proveedor_obj else '') or '',
        "nit": (getattr(proveedor_obj, 'nit', '') if proveedor_obj else '') or '',
        "contacto": '',
        "correo": (getattr(proveedor_obj, 'correo', '') if proveedor_obj else '') or '',
        "telefono": (getattr(proveedor_obj, 'telefono', '') if proveedor_obj else '') or '',
    }

    # Calcular IVA por ítem si no existe, usando IVA del SKU (afecto => 12%)
    detalles_ctx = []
    total_sin_iva = Decimal('0')
    total_iva = Decimal('0')
    total_con_iva = Decimal('0')
    for it in items:
        precio_sin_iva = Decimal(it.precio_sin_iva or 0)
        cantidad = Decimal(it.cantidad or 0)
        iva_unit = Decimal(it.iva or 0)
        if iva_unit == 0 and it.codigo_sku and it.codigo_sku != 'SERV':
            try:
                sku = InventarioSKU.objects.filter(codigo_sku=it.codigo_sku).only('iva').first()
                if sku and (sku.iva or '').lower() == 'afecto':
                    iva_unit = (precio_sin_iva * Decimal('0.12')).quantize(Decimal('0.01'))
            except Exception:
                pass
        total_unit = precio_sin_iva + iva_unit
        total_item = (total_unit * cantidad).quantize(Decimal('0.01'))
        detalles_ctx.append({
            "codigo_sku": it.codigo_sku,
            "descripcion": it.descripcion or '',
            "cantidad": float(cantidad),
            "unidad_medida": it.unidad_medida or '',
            "precio_sin_iva": float(precio_sin_iva),
            "iva": float(iva_unit),
            "total": float(total_item),
        })
        total_sin_iva += (precio_sin_iva * cantidad)
        total_iva += (iva_unit * cantidad)
        total_con_iva += total_item

    orden_ctx = {
        "numero": oc.numero or str(oc.id),
        "fecha": oc.fecha_creacion.strftime('%Y-%m-%d') if oc.fecha_creacion else None,
        "estado": oc.estatus,
        "impreso_por": getattr(request.user, 'username', '') if request.user.is_authenticated else '',
        "fecha_impresion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "proveedor": proveedor_ctx,
        "facturar_a": {
            "nombre": "Servicios Medicos Integrados el Naranjo,S.A.",
            "direccion": "Bulevar El Naranjo 22-40, Colonia El Naranjo Zona 4 de Mixco, Guatemala Ciudad",
            "nit": "66784395",
        },
        "forma_pago": ("Crédito" if oc.condiciones_pago == 'CREDITO' else ("Contado" if oc.condiciones_pago == 'CONTADO' else None)),
        "dias_credito": oc.dias_credito,
        "forma_entrega": "",  # dejar vacío en PDF si no se define
        "tiempo_entrega": "",
        "items": detalles_ctx,
        "total_sin_iva": float(total_sin_iva),
        "iva": float(total_iva),
        "total_con_iva": float(total_con_iva),
        "recepcion": {
            "fecha_entrega": oc.fecha_entrega.strftime('%Y-%m-%d') if oc.fecha_entrega else "",
            "observaciones": "",
            "responsable": "",
            "telefono": "",
            "departamento": "",
        },
        "nota_importante": None,
    }

    html = render_to_string('pdf/orden_compra.html', {"orden": orden_ctx})

    # Intentar con pdfkit/wkhtmltopdf si está disponible
    try:
        import pdfkit  # type: ignore

        cmd = os.getenv('PDFKIT_CMD')
        config = pdfkit.configuration(wkhtmltopdf=cmd) if cmd else None
        options = {"enable-local-file-access": None}
        pdf = pdfkit.from_string(html, False, configuration=config, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
    except Exception:
        # Fallback a WeasyPrint (ya está en requirements)
        try:
            from weasyprint import HTML  # type: ignore
            pdf = HTML(string=html, base_url=None).write_pdf()
            response = HttpResponse(pdf, content_type='application/pdf')
        except Exception as e:  # pragma: no cover
            raise Http404(f"No se pudo generar el PDF: {e}")

    filename = f"orden_compra_{(oc.numero or oc.id)}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
