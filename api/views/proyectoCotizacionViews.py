from functools import reduce
import operator as op

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models.proyectoModel import Proyectos
from ..serializers.proyectoSerializer import ProyectoSerializer
from ..models.detalleProyectoModel import DetalleProyectos
from ..serializers.detalleProyectoSerializer import DetalleProyectoSerializer
from django.db.models import Q


from api.utils.pagination import CustomPageNumberPagination


@swagger_auto_schema(method='get', operation_summary="Listar Cotizaciones", tags=["proyectos"])
@api_view(['GET'])
def listar_cotizaciones(request):
    """
    Lista todas las cotizaciones activas.
    """
    proyectos = Proyectos.objects.filter(Q(estatusProyecto=0) | Q(estatusProyecto = 1)).order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(proyectos, request)

    serializer = ProyectoSerializer(result_page, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_summary="Listar productos asociados a un proyecto",
    tags=["proyectos"]
)
@api_view(['GET'])
def listar_productos_por_proyecto(request, proyecto_id):
    """
    Lista todos los productos asociados a un proyecto.
    """
    try:
        proyecto = Proyectos.objects.get(id=proyecto_id)
    except Proyectos.DoesNotExist:
        return Response(
            {"error": "Proyecto no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    detalles = DetalleProyectos.objects.filter(proyectoId=proyecto)
    serializer = DetalleProyectoSerializer(detalles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=ProyectoSerializer, operation_summary="Crear nueva cotización desde Landingpage", tags=["proyectos"])
@api_view(['POST'])
def crear_cotizacion(request):
    """
    Crea una nueva cotización desde landing page o portal admin.
    """
    print(request.data)
    serializer = ProyectoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=ProyectoSerializer, operation_summary="Actualizar cotización", tags=["proyectos"])
@api_view(['PUT'])
def actualizar_cotizacion(request, pk):
    """
    Actualiza una cotización por ID.
    """
    try:
        proyecto = Proyectos.objects.get(pk=pk, is_active=True)
    except Proyectos.DoesNotExist:
        return Response({"error": "Cotización no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    print("🔍 Datos recibidos:", request.data)
    serializer = ProyectoSerializer(proyecto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("❌ Errores del serializer:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=ProyectoSerializer, operation_summary="Cotización/Proyecto rechazado", tags=["proyectos"])
@api_view(['PUT'])
def cotización_cancelada(request, pk):
    """
    Rechaza proyecto o cotización por id.
    """
    try:
        proyecto = Proyectos.objects.get(pk=pk)
    except Proyectos.DoesNotExist:
        return Response({"error": "Cotización no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    print("🔍 Datos recibidos:", request.data)
    serializer = ProyectoSerializer(proyecto, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("❌ Errores del serializer:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)