from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination #hacer un archivo general para paginacion
from rest_framework import status
from collections import defaultdict
from rest_framework.generics import get_object_or_404

from api.utils.pagination import CustomPageNumberPagination
from ..models.habitacionModel import Habitacion
from ..serializers.habitacionSerializer import (
    HabitacionSerializer
)

@api_view(['POST'])
def crear_habitacion(request):
    serializer = HabitacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listar_habitaciones(request):
    habitaciones = Habitacion.objects.all().order_by('id')
    paginator = CustomPageNumberPagination()
    resultado = paginator.paginate_queryset(habitaciones, request)

    data = []
    for habitacion in resultado:
        data.append({
            "id": habitacion.id,
            "codigo": habitacion.codigo,
            "area": habitacion.area,
            "estado": habitacion.estado,
            "admision": habitacion.admision,
            "paciente": habitacion.paciente,
            "nivel": habitacion.nivel
        })

    return paginator.get_paginated_response(data)

@api_view(['GET'])
def listar_all_habitaciones(request):
    habitaciones = Habitacion.objects.all().order_by('id')

    data = []
    for habitacion in habitaciones:
        data.append({
            "id": habitacion.id,
            "codigo": habitacion.codigo,
            "area": habitacion.area,
            "estado": habitacion.estado,
            "admision": habitacion.admision,
            "paciente": habitacion.paciente,
            "nivel": habitacion.nivel
        })

    return Response(data)