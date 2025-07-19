from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.inventarioBodegasModel import Bodegas, Cajero
from ..serializers.inventarioBodegasSerializer import BodegaSerializer, CajeroSerializer
from api.utils.pagination import CustomPageNumberPagination


@api_view(['POST'])
def crear_cajero(request):
    serializer = CajeroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_cajero_por_clave(request, clave):
    try:
        cajero = Cajero.objects.select_related('bodega').get(clave=clave, esta_activo=True)
        return Response({
            "cajero_id": cajero.id,
            "nombre": cajero.nombre,
            "bodega_id": cajero.bodega.id,
            "bodega_nombre": cajero.bodega.nombre
        })
    except Cajero.DoesNotExist:
        return Response({"error": "Clave inválida o cajero inactivo"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def listar_cajeros(request):
    cajeros = Cajero.objects.select_related('bodega').order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(cajeros, request)
    serializer = CajeroSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
