from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.utils.pagination import CustomPageNumberPagination
from ..models.historialApiModel import HistorialAPI
from ..serializers.historialApiSerializer import HistorialAPISerializer
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils.timezone import now, localtime
import os
from django.conf import settings
from ..models.inventariosSkuModel import InventarioSKU

User = get_user_model()

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def listar_historial_api(request):
    queryset = HistorialAPI.objects.values(
        'id', 'fecha', 'endpoint', 'descripcion', 'usuario__username', 'metodo', 'exito', 'codigo_respuesta'
    )

    modulo = request.GET.get('modulo')
    if modulo:
        queryset = queryset.filter(endpoint__icontains=modulo)

    tipo = request.GET.get('tipo')
    if tipo == 'movimiento':
        queryset = queryset.filter(
            Q(endpoint__icontains='/skus/mover/') |
            Q(descripcion__icontains='se movieron')
        )

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(fecha__range=(inicio, fin))
        except ValueError:
            return Response({'error': 'Fechas con formato inválido. Use YYYY-MM-DD.'}, status=400)

    queryset = queryset.order_by('fecha')

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)

    return Response({
        "count": paginator.page.paginator.count,
        "total_pages": paginator.page.paginator.num_pages,
        "current_page": paginator.page.number,
        "page_size": paginator.get_page_size(request),
        "from": paginator.page.start_index(),
        "to": paginator.page.end_index(),
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": list(result_page),
    })
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def exportar_historial_pdf(request):
    queryset = HistorialAPI.objects.all().order_by('fecha')

    modulo = request.GET.get('modulo')
    if modulo:
        queryset = queryset.filter(endpoint__icontains=modulo)

    tipo = request.GET.get('tipo')
    if tipo == 'movimiento':
        queryset = queryset.filter(
            Q(endpoint__icontains='/skus/mover/') |
            Q(descripcion__icontains='se movieron')
        )

    fecha_inicio = request.GET.get('fecha_inicio')
    if fecha_inicio:
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            queryset = queryset.filter(fecha__date__gte=inicio)
        except ValueError:
            return HttpResponse('Formato de fecha_inicio inválido. Use YYYY-MM-DD.', status=400)

    fecha_fin = request.GET.get('fecha_fin')
    if fecha_fin:
        try:
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(fecha__lt=fin)
        except ValueError:
            return HttpResponse('Formato de fecha_fin inválido. Use YYYY-MM-DD.', status=400)

    historial = list(queryset.values(
        'usuario__username', 'endpoint', 'metodo', 'fecha', 'descripcion'
    ))

    logo_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'img', 'el-naranjo.png')

    filtros = {
        'módulo': modulo or 'Todos',
        'tipo': tipo or 'Todos',
        'fecha_inicio': fecha_inicio or 'Sin filtro',
        'fecha_fin': fecha_fin or 'Sin filtro',
    }

    fecha_generado = localtime(now()).strftime('%Y-%m-%d %H:%M')

    html_string = render_to_string('reporte_historial.html', {
        'historial': historial,
        'logo_path': f'file://{logo_path}',
        'filtros': filtros,
        'fecha_generado': fecha_generado,
    })

    pdf = HTML(string=html_string).write_pdf()

    fecha_inicio_str = fecha_inicio or 'inicio'
    fecha_fin_str = fecha_fin or localtime(now()).strftime('%Y-%m-%d')
    nombre_archivo = f"historial_api_{fecha_inicio_str}_a_{fecha_fin_str}.pdf".replace(":", "-")

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def exportar_usuarios_pdf(request):
    usuarios = User.objects.all().order_by('username')

    data = list(usuarios.values(
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active'
    ))

    logo_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'img', 'el-naranjo.png')

    html_string = render_to_string('reporte_usuarios.html', {
        'usuarios': data,
        'logo_path': f'file://{logo_path}',
        'fecha_generado': localtime(now()).strftime('%Y-%m-%d %H:%M'),
    })

    pdf = HTML(string=html_string).write_pdf()

    nombre_archivo = f"usuarios_{localtime(now()).strftime('%Y-%m-%d_%H-%M')}.pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response

@api_view(['GET'])
def exportar_skus_pdf(request):
    skus = InventarioSKU.objects.all().order_by('id')

    data = [
        {
            'id': sku.id,
            'codigo': sku.codigo_sku,
            'nombre': sku.nombre,
            'marca': sku.marca,
            'medida': sku.unidad_despacho,
            'categoria': sku.categoria,
            'subcategoria': sku.subcategoria or '',
            'estado': sku.estado.upper(),
        }
        for sku in skus
    ]

    logo_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'img', 'el-naranjo.png')

    html_string = render_to_string('reporte_inventario.html', {
        'skus': data,
        'logo_path': f'file://{logo_path}',
        'fecha_generado': localtime(now()).strftime('%Y-%m-%d %H:%M'),
    })

    pdf = HTML(string=html_string).write_pdf()

    nombre_archivo = f"reporte_skus_{localtime(now()).strftime('%Y-%m-%d_%H-%M')}.pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response