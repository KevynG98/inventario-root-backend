from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from collections import defaultdict
from ..models.admisionesModel import Admision, Habitacion
from ..serializers.admisionesSerializer import (
    AdmisionCreateSerializer,
    AdmisionUpdateFlatSerializer,
    AdmisionDetalleSerializer,
    HabitacionSerializer
)

# 🔹 Crear admisión (POST - datos planos)
@api_view(['POST'])
def crear_admision(request):
    serializer = AdmisionCreateSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        admision = serializer.save()
        return Response({"message": "Admisión creada correctamente", "id": admision.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Obtener admisión por ID (GET)
@api_view(['GET'])
def obtener_admision(request, admision_id):
    try:
        admision = Admision.objects.get(pk=admision_id)
    except Admision.DoesNotExist:
        return Response({"error": "Admisión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdmisionDetalleSerializer(admision)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 🔹 Listar agrupadas por área (GET - sin paginación)
@api_view(['GET'])
def listar_admisiones_por_area(request):
    admisiones = Admision.objects.select_related('paciente').all()
    agrupadas = defaultdict(list)
    for admision in admisiones:
        serialized = AdmisionDetalleSerializer(admision).data
        area = admision.area_admision or "Sin área"
        agrupadas[area].append(serialized)
    return Response(agrupadas, status=status.HTTP_200_OK)

# 🔹 Resumen por área (GET - sin paginación)
@api_view(['GET'])
def resumen_admisiones_por_area(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').all()
    agrupadas = defaultdict(list)
    for admision in admisiones:
        paciente = admision.paciente
        area = admision.area_admision or "Sin área"
        resumen = {
            "id_admision": admision.id,
            "fecha_admision": admision.fecha.strftime('%Y-%m-%d'),
            "paciente": paciente.nombre,
            "identificacion": paciente.numero_identificacion,
            "genero": getattr(paciente, "genero", "N/A"),
            "aseguradora": admision.datos_seguro.aseguradora if admision.datos_seguro else "N/A",
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico_tratante": admision.medico_tratante
        }
        agrupadas[area].append(resumen)
    return Response(agrupadas, status=status.HTTP_200_OK)

# 🔹 Paginación global para resumen
class AdmisionResumenPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'

@api_view(['GET'])
def listar_admisiones_resumen(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').order_by('-fecha')
    paginator = AdmisionResumenPagination()
    resultado = paginator.paginate_queryset(admisiones, request)

    data = []
    for admision in resultado:
        paciente = admision.paciente
        data.append({
            "id_admision": admision.id,
            "fecha_admision": admision.fecha.strftime('%d/%m/%Y'),
            "paciente": " ".join(f"{paciente.primer_nombre} {paciente.segundo_nombre or ''} {paciente.primer_apellido} {paciente.segundo_apellido or ''} {paciente.apellido_casada or ''}".split()) + f" (Edad: {paciente.edad} NAC: {paciente.fecha_nacimiento})",
            "identificacion": f"{paciente.tipo_identificacion}: {paciente.numero_identificacion}",
            "genero": getattr(paciente, "genero", "N/D"),
            "aseguradora": admision.datos_seguro.aseguradora if admision.datos_seguro else "SIN SEGURO",
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico_tratante": admision.medico_tratante
        })

    return paginator.get_paginated_response(data)

# 🔹 Editar admisión (PUT - datos anidados)
@api_view(['PUT'])
def editar_admision(request, pk):
    try:
        admision = Admision.objects.get(pk=pk)
    except Admision.DoesNotExist:
        return Response({'error': 'Admisión no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdmisionUpdateFlatSerializer(admision, data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Admisión actualizada correctamente"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#HABITACIONES INICIO
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
    paginator = AdmisionResumenPagination()
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
def listar_admisiones_estado(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').order_by('-fecha')

    data = []
    for admision in admisiones:
        paciente = admision.paciente
        datos_seguro = admision.datos_seguro

        data.append({
            "id_admision": admision.id,
            "fecha_admision": admision.fecha.strftime('%d/%m/%Y') if admision.fecha else '',
            "paciente": " ".join(f"{paciente.primer_nombre} {paciente.segundo_nombre or ''} {paciente.primer_apellido} {paciente.segundo_apellido or ''} {paciente.apellido_casada or ''}".split()),
            "identificacion": f"{paciente.tipo_identificacion}: {paciente.numero_identificacion}",
            "genero": paciente.genero,
            "aseguradora": datos_seguro.aseguradora if datos_seguro else '',
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico": admision.medico_tratante,
            "estado": admision.estado,
        })

    return Response(data)

# 🔹 ListView (no modificada)
class ListadoAdmisionesView(ListAPIView):
    queryset = Admision.objects.all()
    serializer_class = AdmisionDetalleSerializer
