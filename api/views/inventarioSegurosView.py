from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioSegurosModel import Seguros
from ..serializers.inventarioSegurosSerializer import SegurosSerializer

@api_view(['GET'])
def listar_seguros(request):
    marcas = Seguros.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(marcas, request)
    serializer = SegurosSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def crear_seguros(request):
    serializer = SegurosSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_seguros(request, pk):
    try:
        marca = Seguros.objects.get(pk=pk)
    except Seguros.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SegurosSerializer(marca, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_seguros(request, pk):
    try:
        bodega = Seguros.objects.get(pk=pk)
    except Seguros.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    bodega.is_active = False
    bodega.save()
    return Response({'mensaje': 'Marca eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def obtener_seguros(request, pk):
    try:
        marca = Seguros.objects.get(pk=pk)
        serializer = SegurosSerializer(marca)
        return Response(serializer.data)
    except Seguros.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)
