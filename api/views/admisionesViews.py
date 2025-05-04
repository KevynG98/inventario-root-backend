
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from collections import defaultdict
from ..models.admisionesModel import Admision
from ..serializers.admisionesSerializer import AdmisionSerializer

# Crear admisión
@api_view(['POST'])
def crear_admision(request):
    serializer = AdmisionSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        admision = serializer.save()
        return Response({"message": "Admisión creada correctamente", "id": admision.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener admisión
@api_view(['GET'])
def obtener_admision(request, admision_id):
    try:
        admision = Admision.objects.get(pk=admision_id)
    except Admision.DoesNotExist:
        return Response({"error": "Admisión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdmisionSerializer(admision)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Listar admisiones agrupadas por área (no paginadas)
@api_view(['GET'])
def listar_admisiones_por_area(request):
    admisiones = Admision.objects.select_related('paciente').all()
    agrupadas = defaultdict(list)
    for admision in admisiones:
        serialized = AdmisionSerializer(admision).data
        area = admision.area_admision or "Sin área"
        agrupadas[area].append(serialized)
    return Response(agrupadas, status=status.HTTP_200_OK)

# Resumen por área (no paginado)
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

# Paginado global
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
            "paciente": f"{paciente.nombre} (Edad: {paciente.edad} NAC: {paciente.fecha_nacimiento})",
            "identificacion": f"{paciente.tipo_identificacion}: {paciente.numero_identificacion}",
            "genero": getattr(paciente, "genero", "N/D"),
            "aseguradora": admision.datos_seguro.aseguradora if admision.datos_seguro else "SIN SEGURO",
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico_tratante": admision.medico_tratante
        })

    return paginator.get_paginated_response(data)
