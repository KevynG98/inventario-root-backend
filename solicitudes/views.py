from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DetalleSolicitud, Solicitud
from .serializers import SolicitudSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    queryset = Solicitud.objects.prefetch_related("detalle").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        fecha = request.query_params.get("fecha")
        bodega = request.query_params.get("bodega")
        estatus = request.query_params.get("estatus")

        if fecha:
            queryset = queryset.filter(fecha=fecha)
        if bodega:
            queryset = queryset.filter(
                Q(bodega_origen__icontains=bodega) | Q(bodega_destino__icontains=bodega)
            )
        if estatus:
            queryset = queryset.filter(estatus=estatus)

        return queryset.order_by("-fecha", "-id")

    def perform_create(self, serializer):
        serializer.save(estatus=Solicitud.Estatus.NUEVA)

    @action(detail=True, methods=["patch"], url_path="guardar")
    def guardar(self, request, pk=None):
        solicitud = self.get_object()
        updated = self._update_detalle_from_payload(solicitud, request.data)

        if isinstance(updated, Response):
            return updated

        solicitud.estatus = Solicitud.Estatus.EN_PROCESO
        solicitud.save(update_fields=["estatus"])
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="enviar")
    def enviar(self, request, pk=None):
        solicitud = self.get_object()
        updated = self._update_detalle_from_payload(solicitud, request.data)

        if isinstance(updated, Response):
            return updated

        faltantes = solicitud.detalle.filter(enviada__isnull=True)
        if faltantes.exists():
            return Response(
                {
                    "detalle": "Todos los ítems deben tener cantidad enviada antes de marcar la solicitud como Pendiente de Recibir."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        solicitud.estatus = Solicitud.Estatus.PENDIENTE_RECIBIR
        solicitud.save(update_fields=["estatus"])
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data)

    def _update_detalle_from_payload(self, solicitud: Solicitud, payload):
        detalle_payload = payload.get("detalle", [])
        if detalle_payload is None:
            return None

        if not isinstance(detalle_payload, list):
            return Response(
                {"detalle": "El detalle debe ser una lista de items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        detalle_map = {item.id: item for item in solicitud.detalle.all()}
        to_update = []

        for item in detalle_payload:
            item_id = item.get("id")
            if not item_id or item_id not in detalle_map:
                return Response(
                    {"detalle": f"El ítem con id {item_id} no pertenece a la solicitud."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            detalle_instance = detalle_map[item_id]

            if "enviada" in item:
                enviada_value = item["enviada"]
                if enviada_value is None:
                    detalle_instance.enviada = None
                else:
                    try:
                        enviada_int = int(enviada_value)
                    except (TypeError, ValueError):
                        return Response(
                            {"detalle": "La cantidad enviada debe ser un número entero."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if enviada_int < 0:
                        return Response(
                            {"detalle": "La cantidad enviada no puede ser negativa."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    detalle_instance.enviada = enviada_int

            if "comentario" in item:
                detalle_instance.comentario = item.get("comentario")

            to_update.append(detalle_instance)

        if to_update:
            DetalleSolicitud.objects.bulk_update(to_update, ["enviada", "comentario"])

        return True
