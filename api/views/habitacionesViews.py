from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.generics import get_object_or_404

from api.utils.pagination import CustomPageNumberPagination
from ..models.habitacionModel import Habitacion
from ..serializers.habitacionSerializer import HabitacionSerializer


ESTADOS_DISPONIBLES = {
    'Vacante Inspeccionada -DISPONIBLE-',
    'Vacante Inspeccionada - Disponible',
    'Vacante Inspeccionada -DISPONIBLE',
    'Vacante Inspeccionada - Disponible -',
}

@api_view(['POST'])
def crear_habitacion(request):
    serializer = HabitacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listar_habitaciones(request):
    habitaciones = Habitacion.objects.filter(is_active=True)

    solo_disponibles = request.query_params.get('solo_disponibles')
    if solo_disponibles and solo_disponibles.lower() in {'1', 'true', 't', 'yes', 'si'}:
        habitaciones = habitaciones.filter(
            estado__in=ESTADOS_DISPONIBLES,
            admision__isnull=True
        )

    habitaciones = habitaciones.order_by('area', 'codigo')
    paginator = CustomPageNumberPagination()
    resultado = paginator.paginate_queryset(habitaciones, request)

    serializer = HabitacionSerializer(resultado, many=True)
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

@api_view(['GET'])
def listar_all_habitaciones(request):
    habitaciones = Habitacion.objects.filter(is_active=True)

    solo_disponibles = request.query_params.get('solo_disponibles')
    if solo_disponibles and solo_disponibles.lower() in {'1', 'true', 't', 'yes', 'si'}:
        habitaciones = habitaciones.filter(
            estado__in=ESTADOS_DISPONIBLES,
            admision__isnull=True
        )

    habitaciones = habitaciones.order_by('area')
    serializer = HabitacionSerializer(habitaciones, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    serializer = HabitacionSerializer(habitacion)
    return Response(serializer.data)

@api_view(['PUT'])
def actualizar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    serializer = HabitacionSerializer(habitacion, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    habitacion.is_active = False
    habitacion.save()
    return Response({'mensaje': 'Habitación desactivada correctamente'}, status=status.HTTP_204_NO_CONTENT)
