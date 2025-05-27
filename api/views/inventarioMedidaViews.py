from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.inventarioMedidaModel import Medida
from ..serializers.inventarioMedidaSerializer import MarcaSerializer

@api_view(['GET'])
def listar_medidas(request):
    medidas = Medida.objects.filter(is_active=True).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(medidas, request)
    serializer = MarcaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def crear_medida(request):
    serializer = MarcaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MarcaSerializer(medida, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    medida.is_active = False
    medida.save()
    return Response({'mensaje': 'Medida eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def obtener_medida(request, pk):
    try:
        medida = Medida.objects.get(pk=pk)
        serializer = MarcaSerializer(medida)
        return Response(serializer.data)
    except Medida.DoesNotExist:
        return Response({'error': 'Medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)
