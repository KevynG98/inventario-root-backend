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
        # Resolve username from authenticated user or X-User header
        username = None
        try:
            if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
                username = request.user.username
        except Exception:
            username = None
        if not username:
            username = request.headers.get('X-User') or None

        serializer.save(usuario=username)
        # Para tu middleware de auditoría, si lo usas:
        request.descripcion = f"➕ Requisición #{serializer.data['id']} creada"
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def listar_requisiciones(request):
    estado = request.GET.get('estado')  # puede ser 'aprobada', 'pendiente', etc.
    excluir = request.GET.get('excluir')

    queryset = Requisicion.objects.all()

    if estado:
        queryset = queryset.filter(estado=estado)
    elif excluir:
        queryset = queryset.exclude(estado=excluir)

    serializer = RequisicionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cambiar_estado_requisicion(request, id):
    """
    Cambia únicamente el campo 'estado' de la requisición indicada.
    """
    requisicion = get_object_or_404(Requisicion, id=id)
    serializer = RequisicionEstadoSerializer(requisicion, data=request.data, partial=True)

    if serializer.is_valid():
        # Resolve username for auditoría de cambio de estado
        username = None
        try:
            if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
                username = request.user.username
        except Exception:
            username = None
        if not username:
            username = request.headers.get('X-User') or None

        # Save estado/descripcion
        serializer.save()

        # Set estado_actualizado_por
        requisicion.estado_actualizado_por = username
        requisicion.save(update_fields=['estado_actualizado_por'])

        nuevo_estado = serializer.validated_data.get('estado', requisicion.estado)
        request.descripcion = (
            f"🔄 Requisición #{requisicion.id} cambió a '{nuevo_estado}' por {username or 'N/A'}"
        )
        return Response(
            {"message": "Estado actualizado", "requisicion": RequisicionSerializer(requisicion).data},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_requisicion(request, id):
    """
    Actualiza campos de la requisición e items (productos/servicios).
    Si se envían 'productos' y/o 'servicios', se reemplazan los existentes.
    """
    requisicion = get_object_or_404(Requisicion, id=id)
    partial = request.method == 'PATCH'
    serializer = RequisicionSerializer(requisicion, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        request.descripcion = f"✏️ Requisición #{requisicion.id} actualizada"
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
