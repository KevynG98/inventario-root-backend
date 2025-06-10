from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.directorioModel import Directorio
from ..serializers.directorioSerializer import DirectorioSerializer

@api_view(['GET'])
def listar_directorio(request):
    marcas = Directorio.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(marcas, request)
    serializer = DirectorioSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def crear_directorio(request):
    serializer = DirectorioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_directorio(request, pk):
    try:
        marca = Directorio.objects.get(pk=pk)
    except Directorio.DoesNotExist:
        return Response({'error': 'Directorio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DirectorioSerializer(marca, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_directorio(request, pk):
    try:
        bodega = Directorio.objects.get(pk=pk)
    except Directorio.DoesNotExist:
        return Response({'error': 'Directorio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    bodega.is_active = False
    bodega.save()
    return Response({'mensaje': 'Directorio eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def obtener_directorio(request, pk):
    try:
        marca = Directorio.objects.get(pk=pk)
        serializer = DirectorioSerializer(marca)
        return Response(serializer.data)
    except Directorio.DoesNotExist:
        return Response({'error': 'Directorio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
