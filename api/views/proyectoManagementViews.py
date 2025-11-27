from functools import reduce
import operator as op

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi  # type: ignore

from ..models.proyectoModel import Proyectos
from ..serializers.proyectoSerializer import ProyectoSerializer

from api.utils.pagination import CustomPageNumberPagination

@swagger_auto_schema(method='get', operation_summary="Listar Proyectos", tags=["proyectos"])
@api_view(['GET'])
def listar_pryectos(request):
    """
    Lista de proyectos que no son cotizaciones.
    """
    search = request.query_params.get('search')
    
    if search is not None:
        proyectos = Proyectos.objects.filter(
            (~Q(estatusProyecto=0) & ~Q(estatusProyecto=1) & ~Q(estatusProyecto = 2)) &
            (Q(estatusProyecto__icontains=search))
        ).order_by('id')
    else:
        proyectos = Proyectos.objects.filter(~Q(estatusProyecto=0) & 
        ~Q(estatusProyecto = 1) & ~Q(estatusProyecto = 2)).order_by('id')
    
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(proyectos, request)

    serializer = ProyectoSerializer(result_page, many=True)
    return Response(serializer.data) 




@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'estatus': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Estatus a actualizar el proyecto',
            ),
        },
        required=['id'],
    ),
    operation_summary="Cambio de estatus del proyecto",
    tags=["proyectos"],
)
@api_view(['PUT'])
def actualizar_estatus_proyecto(request):
    """
    Actualiza el estatus del proyecto.
    
    Body esperado:
    {
        "estatus": number,
        "id": number
    }
    """
    # Validar que enviaron el campo
    nuevo_estatus = request.data.get("estatus")
    proyecto_id = request.data.get("id")

    if nuevo_estatus is None:
        return Response(
            {"error": "El campo 'estatus' es requerido."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Verificar si es número
    try:
        nuevo_estatus = int(nuevo_estatus)
    except ValueError:
        return Response(
            {"error": "El campo 'estatus' debe ser un número entero."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Obtener lista de estatus válidos
    estatus_validos = [opcion[0] for opcion in Proyectos.ESTATUS_CHOICES]

    # Validar si está dentro de opciones permitidas
    if nuevo_estatus not in estatus_validos:
        return Response(
            {
                "error": f"El estatus '{nuevo_estatus}' no es válido.",
                "estatus_permitidos": estatus_validos,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Buscar proyecto
    try:
        proyecto = Proyectos.objects.get(pk=proyecto_id)
    except Proyectos.DoesNotExist:
        return Response(
            {"error": "Proyecto no encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Actualizar estatus
    proyecto.estatusProyecto = nuevo_estatus
    proyecto.save()

    return Response(
        {
            "mensaje": "Estatus actualizado correctamente.",
            "proyectoId": proyecto_id,
            "estatusNuevo": nuevo_estatus,
        },
        status=status.HTTP_200_OK,
    )
