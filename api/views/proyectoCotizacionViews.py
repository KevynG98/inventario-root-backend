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

@swagger_auto_schema(method='get', operation_summary="Listar Cotizaciones", tags=["proyectos"])
@api_view(['GET'])
def listar_cotizaciones_rechazadas(request):
    """
    Lista todas las cotizaciones activas.
    """
    proyectos = Proyectos.objects.filter(Q(estatusProyecto=2)).order_by('id')
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

@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID del proyecto/cotización a rechazar',
            ),
        },
        required=['id'],
    ),
    operation_summary="Cotización/Proyecto rechazado",
    tags=["proyectos"],
)
@api_view(['PUT'])
def cotización_cancelada(request):
    """Rechaza un proyecto o cotización cambiando su estatus a 2 (RECHAZADO).

    Body esperado: 
    {
        "id": number
    }
    """
    proyecto_id = request.data.get('id')

    if proyecto_id is None:
        return Response(
            {"error": "El campo 'id' es requerido."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        proyecto = Proyectos.objects.get(pk=proyecto_id)
    except Proyectos.DoesNotExist:
        return Response(
            {"error": "Cotización no encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Cambiar el estatus del proyecto a RECHAZADO (2)
    proyecto.estatusProyecto = Proyectos.RECHAZADO
    proyecto.save()

    serializer = ProyectoSerializer(proyecto)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID del proyecto/aprobarcotizacion a aprobar',
            ),
        },
        required=['id'],
    ),
    operation_summary="Cotización/Proyecto Aprobado",
    tags=["proyectos"],
)
@api_view(['PUT'])
def cotizacion_aprobada(request):
    """Aprueba un proyecto o cotización cambiando su estatus a 3 (ACEPTADO).

    Body esperado: 
    {
        "id": number
    }
    """    
    proyecto_id = request.data.get('id')
    
    
    try:
        proyecto = Proyectos.objects.get(pk=proyecto_id)
    except Proyectos.DoesNotExist:
        return Response(
            {"error": "Cotización no encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if proyecto_id is None:
        return Response(
            {"error": "El campo 'id' es requerido."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif proyecto.estatusProyecto == "2":
        return Response(
            {"error": "El ID '2' no es válido para aprobar una cotización."},
            status=status.HTTP_400_BAD_REQUEST,
        )



    # Cambiar el estatus del proyecto a ACEPTADO (3)
    proyecto.estatusProyecto = Proyectos.ACEPTADO
    proyecto.save()

    serializer = ProyectoSerializer(proyecto)
    return Response(serializer.data, status=status.HTTP_200_OK)