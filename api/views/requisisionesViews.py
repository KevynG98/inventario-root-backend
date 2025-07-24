# requisiciones/views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models.requisisionesModel import Requisicion
from ..serializers.requisisionesSerializer import RequisicionSerializer, RequisicionEstadoSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def guardar_requisicion(request):
    """
    Crea (guarda) una nueva requisición.
    """
    serializer = RequisicionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Para tu middleware de auditoría, si lo usas:
        request.descripcion = f"➕ Requisición #{serializer.data['id']} creada"
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def listar_requisiciones(request):
    """
    Devuelve la lista de todas las requisiciones.
    """
    queryset = Requisicion.objects.all().order_by('-created_at')
    serializer = RequisicionSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cambiar_estado_requisicion(request, id):
    """
    Cambia únicamente el campo 'estado' de la requisición indicada.
    """
    requisicion = get_object_or_404(Requisicion, id=id)
    serializer = RequisicionEstadoSerializer(
        requisicion, data=request.data, partial=True
    )

    if serializer.is_valid():
        serializer.save()
        nuevo_estado = serializer.validated_data.get('estado', requisicion.estado)
        request.descripcion = (
            f"🔄 Requisición #{requisicion.id} cambió a '{nuevo_estado}'"
        )
        return Response(
            {"message": "Estado actualizado", "requisicion": serializer.data},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
