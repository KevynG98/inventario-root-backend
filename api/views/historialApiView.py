from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.utils.pagination import CustomPageNumberPagination
from ..models.historialApiModel import HistorialAPI
from ..serializers.historialApiSerializer import HistorialAPISerializer
from datetime import datetime, timedelta
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_historial_api(request):
    queryset = HistorialAPI.objects.all().order_by('fecha')

    # Filtro por módulo
    modulo = request.GET.get('modulo')
    if modulo:
        queryset = queryset.filter(endpoint__icontains=modulo)

    # Filtro por tipo de operación
    tipo = request.GET.get('tipo')
    if tipo == 'movimiento':
        queryset = queryset.filter(
            Q(endpoint__icontains='/skus/mover/') |
            Q(descripcion__icontains='se movieron')
        )


    # Filtro por fecha de inicio
    fecha_inicio = request.GET.get('fecha_inicio')
    if fecha_inicio:
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            queryset = queryset.filter(fecha__date__gte=inicio)
        except ValueError:
            return Response({'error': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD.'}, status=400)

    # Filtro por fecha de fin
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_fin:
        try:
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(fecha__lt=fin)
        except ValueError:
            return Response({'error': 'Formato de fecha_fin inválido. Use YYYY-MM-DD.'}, status=400)

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = HistorialAPISerializer(result_page, many=True)

    return Response({
        "count": paginator.page.paginator.count,
        "total_pages": paginator.page.paginator.num_pages,
        "current_page": paginator.page.number,
        "page_size": paginator.get_page_size(request),
        "from": paginator.page.start_index(),
        "to": paginator.page.end_index(),
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": serializer.data
    })