from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Operacion
from .serializers import OperacionSerializer


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all().order_by("-fecha", "hora")
    serializer_class = OperacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        fecha = self.request.query_params.get("fecha")
        estatus = self.request.query_params.get("estatus")
        especialidad = self.request.query_params.get("especialidad")

        if fecha:
            queryset = queryset.filter(fecha=fecha)
        if estatus:
            queryset = queryset.filter(estatus=estatus)
        if especialidad:
            queryset = queryset.filter(especialidad__iexact=especialidad)

        return queryset

    def perform_create(self, serializer):
        operacion = serializer.save(estatus=Operacion.Estatus.PROGRAMADO)
        operacion.registrar_historial(
            f"Operación creada con estatus {operacion.estatus}",
            usuario=self._resolve_username(),
        )

    def perform_update(self, serializer):
        instancia = serializer.save()
        instancia.registrar_historial(
            "Operación actualizada",
            usuario=self._resolve_username(),
        )

    @action(detail=True, methods=["patch"], url_path="estatus")
    def actualizar_estatus(self, request, pk=None):
        operacion = self.get_object()
        nuevo_estatus = request.data.get("estatus")
        if not nuevo_estatus:
            return Response(
                {"detail": "Debes enviar el nuevo estatus."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if nuevo_estatus not in dict(Operacion.Estatus.choices):
            return Response(
                {"detail": "Estatus inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        operacion.estatus = nuevo_estatus
        operacion.save(update_fields=["estatus", "actualizado_en"])
        operacion.registrar_historial(
            f"Estatus actualizado a {nuevo_estatus}",
            usuario=self._resolve_username(),
        )
        serializer = self.get_serializer(operacion)
        return Response(serializer.data)

    def _resolve_username(self):
        if self.request.user and self.request.user.is_authenticated:
            return self.request.user.username
        return self.request.headers.get("X-User")
