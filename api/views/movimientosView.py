# views/movimientosView.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.movimientoHistoricoModel import MovimientoHistorico
from ..serializers.MovimientoHistoricoSerializer import MovimientoHistoricoSerializer

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
