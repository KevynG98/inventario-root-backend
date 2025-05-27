from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioBodegasModel import Bodegas
from ..serializers.inventarioBodegasSerializer import BodegaSerializer

@api_view(['GET'])
def listar_bodegas(request):
    marcas = Bodegas.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(marcas, request)
    serializer = BodegaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def crear_bodegas(request):
    serializer = BodegaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_bodegas(request, pk):
    try:
        marca = Bodegas.objects.get(pk=pk)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BodegaSerializer(marca, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_bodegas(request, pk):
    try:
        bodega = Bodegas.objects.get(pk=pk)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    bodega.is_active = False
    bodega.save()
    return Response({'mensaje': 'Marca eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def obtener_bodegas(request, pk):
    try:
        marca = Bodegas.objects.get(pk=pk)
        serializer = BodegaSerializer(marca)
        return Response(serializer.data)
    except Bodegas.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)
