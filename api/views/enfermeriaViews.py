from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from django.db import transaction
from django.utils import timezone

from ..models.enfermeriaModel import (
    AdmisionMedicoTratante,
    AntecedenteClinico,
    ControlMedicamento,
    ControlMedicamentoRegistro,
    EvolucionClinica,
    HistoriaEnfermedad,
    NotaEnfermeria,
    OrdenMedica,
    OrdenMedicaEvento,
    RegistroDieta,
    SignoVitalEmergencia,
    SignoVitalEncamamiento,
    IngestaExcretaDia,
    SolicitudMedicamento,
    SolicitudMedicamentoItem,
)
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU
from ..models.salidasModel import Salida, SalidaItem
from ..models.trasladosModel import Traslado, TrasladoItem
from ..serializers.enfermeriaSerializer import (
    AdmisionMedicoTratanteSerializer,
    AntecedenteClinicoSerializer,
    ControlMedicamentoRegistroSerializer,
    ControlMedicamentoSerializer,
    EvolucionClinicaSerializer,
    HistoriaEnfermedadSerializer,
    NotaEnfermeriaSerializer,
    OrdenMedicaEventoSerializer,
    OrdenMedicaSerializer,
    RegistroDietaSerializer,
    SignoVitalEmergenciaSerializer,
    SignoVitalEncamamientoSerializer,
    IngestaExcretaDiaSerializer,
    SolicitudMedicamentoSerializer,
)


def resolve_username(request):
    if request.user and request.user.is_authenticated:
        return request.user.username
    return request.headers.get("X-User")


def _obtener_sku(sku_code):
    try:
        return InventarioSKU.objects.get(codigo_sku=sku_code)
    except InventarioSKU.DoesNotExist as exc:
        raise PermissionDenied(f"El SKU {sku_code} no existe.") from exc


def _ajustar_stock(origen, destino, sku_obj, cantidad):
    if cantidad <= 0:
        return
    origen_stock = (
        BodegaSKU.objects.select_for_update()
        .filter(sku=sku_obj, nombre_bodega=origen)
        .first()
    )
    if not origen_stock or origen_stock.cantidad < cantidad:
        disponible = origen_stock.cantidad if origen_stock else 0
        raise PermissionDenied(
            f"Stock insuficiente en bodega {origen} para SKU {sku_obj.codigo_sku}. "
            f"Disponible: {disponible}, requerido: {cantidad}"
        )
    origen_stock.cantidad = int(origen_stock.cantidad - cantidad)
    origen_stock.save()

    destino_stock, _ = BodegaSKU.objects.select_for_update().get_or_create(
        sku=sku_obj,
        nombre_bodega=destino,
        defaults={"cantidad": 0},
    )
    destino_stock.cantidad = int(destino_stock.cantidad + cantidad)
    destino_stock.save()


def _crear_traslado_recibido(solicitud: SolicitudMedicamento, username: str):
    ahora = timezone.now()
    traslado = Traslado.objects.create(
        bodega_origen=solicitud.bodega_origen,
        bodega_destino=solicitud.bodega_destino,
        comentarios=f"Traslado generado desde solicitud #{solicitud.pk}",
        departamento=None,
        enviado_por=solicitud.enviado_por or username,
        entregamos_a=username,
        recibido_por=username,
        estatus="RECIBIDO",
        fecha_envio=ahora,
        fecha_recibido=ahora,
    )

    for item in solicitud.items.filter(devuelto=False):
        cantidad = item.cantidad_recibida or item.cantidad_enviada or item.cantidad_pedida
        if cantidad <= 0:
            continue
        sku_obj = _obtener_sku(item.sku)
        _ajustar_stock(
            solicitud.bodega_origen,
            solicitud.bodega_destino,
            sku_obj,
            int(cantidad),
        )
        TrasladoItem.objects.create(
            traslado=traslado,
            sku=item.sku,
            descripcion=item.descripcion or sku_obj.nombre,
            cantidad=int(cantidad),
        )

    return traslado


def _crear_traslado_enviado(origen, destino, items, username, departamento=None, entregamos_a=None):
    traslado = Traslado.objects.create(
        bodega_origen=origen,
        bodega_destino=destino,
        comentarios="Traslado generado automáticamente por enfermería",
        departamento=departamento,
        enviado_por=username,
        entregamos_a=entregamos_a,
        estatus="ENVIADO",
        fecha_envio=timezone.now(),
    )
    for item in items:
        sku_obj = _obtener_sku(item["sku"])
        cantidad = int(item.get("cantidad") or 0)
        if cantidad <= 0:
            continue
        origen_stock = (
            BodegaSKU.objects.select_for_update()
            .filter(sku=sku_obj, nombre_bodega=origen)
            .first()
        )
        if not origen_stock or origen_stock.cantidad < cantidad:
            disponible = origen_stock.cantidad if origen_stock else 0
            raise PermissionDenied(
                f"Stock insuficiente en {origen} para SKU {sku_obj.codigo_sku}. "
                f"Disponible: {disponible}, requerido: {cantidad}."
            )
        origen_stock.cantidad = int(origen_stock.cantidad - cantidad)
        origen_stock.save()
        TrasladoItem.objects.create(
            traslado=traslado,
            sku=sku_obj.codigo_sku,
            descripcion=item.get("descripcion") or sku_obj.nombre,
            cantidad=cantidad,
        )
    return traslado


def _crear_salida_paciente(solicitud: SolicitudMedicamento, items, username: str):
    salida = Salida.objects.create(
        bodega=solicitud.bodega_destino,
        tipo_salida="paciente",
        observaciones=f"Salida generada desde solicitud #{solicitud.pk}",
        area=None,
        admision=solicitud.admision_id,
        usuario=username,
        aplicado_por=username,
    )
    for item in items:
        sku_obj = _obtener_sku(item["sku"])
        cantidad = int(item["cantidad"])
        bodega_stock = (
            BodegaSKU.objects.select_for_update()
            .filter(sku=sku_obj, nombre_bodega=solicitud.bodega_destino)
            .first()
        )
        if not bodega_stock or bodega_stock.cantidad < cantidad:
            disponible = bodega_stock.cantidad if bodega_stock else 0
            raise PermissionDenied(
                f"Stock insuficiente en {solicitud.bodega_destino} para SKU {sku_obj.codigo_sku}. "
                f"Disponible: {disponible}, requerido: {cantidad}."
            )
        bodega_stock.cantidad = int(bodega_stock.cantidad - cantidad)
        bodega_stock.save()

        SalidaItem.objects.create(
            salida=salida,
            sku=sku_obj.codigo_sku,
            descripcion=item.get("descripcion") or sku_obj.nombre,
            cantidad=cantidad,
            costo=0,
            precio_sin_iva=0,
            iva=0,
            total=0,
        )
    return salida


class AdmisionScopedViewSet(viewsets.ModelViewSet):
    """
    Base viewset that filters by ?admision=<id> and sets audit fields.
    """

    permission_classes = [IsAuthenticated]
    admision_lookup_param = "admision"

    def get_queryset(self):
        queryset = super().get_queryset()
        admision_id = self.request.query_params.get(self.admision_lookup_param)
        if admision_id:
            queryset = queryset.filter(admision=admision_id)
        return queryset

    def perform_create(self, serializer):
        username = resolve_username(self.request)
        extra = {}
        if "creado_por" in serializer.fields:
            extra["creado_por"] = username
        if "actualizado_por" in serializer.fields:
            extra["actualizado_por"] = username
        serializer.save(**extra)

    def perform_update(self, serializer):
        username = resolve_username(self.request)
        extra = {}
        if "actualizado_por" in serializer.fields:
            extra["actualizado_por"] = username
        serializer.save(**extra)


class AdmisionMedicoTratanteViewSet(AdmisionScopedViewSet):
    queryset = AdmisionMedicoTratante.objects.all().order_by("-creado_en")
    serializer_class = AdmisionMedicoTratanteSerializer


class HistoriaEnfermedadView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, admision_id):
        return HistoriaEnfermedad.objects.filter(admision=admision_id).first()

    def get(self, request, admision_id):
        instance = self.get_object(admision_id)
        if not instance:
            instance = HistoriaEnfermedad.objects.create(admision_id=admision_id)
        serializer = HistoriaEnfermedadSerializer(instance)
        return Response(serializer.data)

    def put(self, request, admision_id):
        instance = self.get_object(admision_id)
        if not instance:
            instance = HistoriaEnfermedad.objects.create(admision_id=admision_id)
        serializer = HistoriaEnfermedadSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        username = resolve_username(request)
        serializer.save(actualizado_por=username)
        return Response(serializer.data)

    patch = put


class SignoVitalEmergenciaViewSet(AdmisionScopedViewSet):
    queryset = SignoVitalEmergencia.objects.all().order_by("-tomado_en")
    serializer_class = SignoVitalEmergenciaSerializer


class SignoVitalEncamamientoViewSet(AdmisionScopedViewSet):
    queryset = SignoVitalEncamamiento.objects.all().order_by("-tomado_en")
    serializer_class = SignoVitalEncamamientoSerializer


class AntecedenteClinicoViewSet(AdmisionScopedViewSet):
    queryset = AntecedenteClinico.objects.all().order_by("-registrado_en")
    serializer_class = AntecedenteClinicoSerializer

    def perform_create(self, serializer):
        username = resolve_username(self.request)
        serializer.save(registrado_por=username)

    def perform_update(self, serializer):
        serializer.save()


class ControlMedicamentoViewSet(AdmisionScopedViewSet):
    queryset = ControlMedicamento.objects.all().order_by("-creado_en")
    serializer_class = ControlMedicamentoSerializer


class SolicitudMedicamentoViewSet(AdmisionScopedViewSet):
    queryset = SolicitudMedicamento.objects.all().order_by("-fecha_creacion")
    serializer_class = SolicitudMedicamentoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("items")

    @action(detail=True, methods=["post"], url_path="enviar")
    def enviar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estatus != SolicitudMedicamento.Estados.PENDIENTE_ENVIAR:
            return Response(
                {"error": "Solo puedes enviar solicitudes pendientes de enviar."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not solicitud.items.exists():
            return Response(
                {"error": "Agrega al menos un SKU antes de enviar la solicitud."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = resolve_username(request)
        solicitud.estatus = SolicitudMedicamento.Estados.ENVIADA
        solicitud.fecha_envio = timezone.now()
        solicitud.enviado_por = username
        solicitud.actualizado_por = username
        solicitud.save(update_fields=["estatus", "fecha_envio", "enviado_por", "actualizado_por", "fecha_actualizacion"])
        return Response(self.get_serializer(solicitud).data)

    @action(detail=True, methods=["post"], url_path="marcar-pendiente-recibir")
    def marcar_pendiente_recibir(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estatus not in (
            SolicitudMedicamento.Estados.ENVIADA,
            SolicitudMedicamento.Estados.PENDIENTE_RECIBIR,
        ):
            return Response(
                {"error": "Solo puedes marcar solicitudes enviadas como pendientes de recibir."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        solicitud.estatus = SolicitudMedicamento.Estados.PENDIENTE_RECIBIR
        solicitud.save(update_fields=["estatus", "fecha_actualizacion"])
        return Response(self.get_serializer(solicitud).data)

    @action(detail=True, methods=["post"], url_path="recibir")
    @transaction.atomic
    def recibir(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estatus not in (
            SolicitudMedicamento.Estados.ENVIADA,
            SolicitudMedicamento.Estados.PENDIENTE_RECIBIR,
        ):
            return Response(
                {"error": "La solicitud debe estar Enviada o Pendiente de Recibir."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if solicitud.traslado_recibo_id:
            return Response(
                {"error": "Esta solicitud ya tiene un traslado registrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        items_payload = request.data.get("items", [])
        payload_map = {item.get("id"): item for item in items_payload if item.get("id")}
        items = list(solicitud.items.filter(devuelto=False))
        if not items:
            return Response({"error": "No hay ítems para recibir."}, status=status.HTTP_400_BAD_REQUEST)

        for item in items:
            data = payload_map.get(item.id, {})
            marcado = data.get("recibido", True)
            cantidad = int(data.get("cantidad_recibida", item.cantidad_enviada or item.cantidad_pedida or 0))
            if not marcado:
                return Response({"error": f"Debes marcar el SKU {item.sku} como recibido."}, status=status.HTTP_400_BAD_REQUEST)
            if cantidad <= 0:
                return Response({"error": f"La cantidad recibida para {item.sku} debe ser mayor a cero."}, status=status.HTTP_400_BAD_REQUEST)
            item.cantidad_recibida = cantidad
            if item.cantidad_enviada == 0:
                item.cantidad_enviada = cantidad
            item.recibido = True
            item.save(update_fields=["cantidad_recibida", "cantidad_enviada", "recibido", "actualizado_en"])

        username = resolve_username(request)
        traslado = _crear_traslado_recibido(solicitud, username or solicitud.recibido_por or solicitud.enviado_por or "Sistema")
        solicitud.estatus = SolicitudMedicamento.Estados.RECIBIDA
        solicitud.recibido_por = username
        solicitud.fecha_recibido = timezone.now()
        solicitud.traslado_recibo = traslado
        solicitud.actualizado_por = username
        solicitud.save(
            update_fields=[
                "estatus",
                "recibido_por",
                "fecha_recibido",
                "traslado_recibo",
                "actualizado_por",
                "fecha_actualizacion",
            ]
        )
        return Response(self.get_serializer(solicitud).data)

    @action(detail=True, methods=["post"], url_path="cargar-estado-cuenta")
    @transaction.atomic
    def cargar_estado_cuenta(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estatus != SolicitudMedicamento.Estados.RECIBIDA:
            return Response(
                {"error": "Solo las solicitudes recibidas pueden cargarse al estado de cuenta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if solicitud.salida_cuenta_id:
            return Response(
                {"error": "Esta solicitud ya se cargó al estado de cuenta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        items = []
        for item in solicitud.items.filter(devuelto=False):
            cantidad = int(item.cantidad_recibida - item.cantidad_devuelta)
            if cantidad <= 0:
                continue
            items.append({"sku": item.sku, "descripcion": item.descripcion, "cantidad": cantidad})
        if not items:
            return Response({"error": "No hay ítems disponibles para cargar al estado de cuenta."}, status=status.HTTP_400_BAD_REQUEST)
        username = resolve_username(request)
        salida = _crear_salida_paciente(solicitud, items, username or solicitud.cargado_por or solicitud.recibido_por or "Sistema")
        solicitud.estatus = SolicitudMedicamento.Estados.CARGADA_EC
        solicitud.salida_cuenta = salida
        solicitud.cargado_por = username
        solicitud.fecha_cargado_ec = timezone.now()
        solicitud.actualizado_por = username
        solicitud.save(
            update_fields=[
                "estatus",
                "salida_cuenta",
                "cargado_por",
                "fecha_cargado_ec",
                "actualizado_por",
                "fecha_actualizacion",
            ]
        )
        return Response(self.get_serializer(solicitud).data)

    @action(detail=True, methods=["post"], url_path="anular")
    @transaction.atomic
    def anular(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estatus == SolicitudMedicamento.Estados.CARGADA_EC:
            return Response({"error": "No es posible anular una solicitud ya cargada al estado de cuenta."}, status=status.HTTP_400_BAD_REQUEST)
        username = resolve_username(request)
        items = []
        if solicitud.estatus == SolicitudMedicamento.Estados.RECIBIDA:
            for item in solicitud.items.filter(devuelto=False):
                cantidad = int(item.cantidad_recibida - item.cantidad_devuelta)
                if cantidad <= 0:
                    continue
                items.append(
                    {
                        "sku": item.sku,
                        "descripcion": item.descripcion,
                        "cantidad": cantidad,
                    }
                )
            if items:
                traslado = _crear_traslado_enviado(
                    solicitud.bodega_destino,
                    solicitud.bodega_origen,
                    items,
                    username or "Sistema",
                    departamento=request.data.get("departamento"),
                    entregamos_a=request.data.get("entregamos_a"),
                )
                solicitud.traslado_recibo = traslado

        solicitud.estatus = SolicitudMedicamento.Estados.ANULADA
        solicitud.actualizado_por = username
        solicitud.save(update_fields=["estatus", "traslado_recibo", "actualizado_por", "fecha_actualizacion"])
        return Response(self.get_serializer(solicitud).data)

    @action(detail=True, methods=["post"], url_path="items/(?P<item_id>[^/.]+)/devolver")
    @transaction.atomic
    def devolver_item(self, request, pk=None, item_id=None):
        solicitud = self.get_object()
        if solicitud.estatus not in (
            SolicitudMedicamento.Estados.RECIBIDA,
            SolicitudMedicamento.Estados.CARGADA_EC,
        ):
            return Response(
                {"error": "Solo puedes devolver ítems de solicitudes recibidas."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            item = solicitud.items.get(pk=item_id)
        except SolicitudMedicamentoItem.DoesNotExist:
            return Response({"error": "Ítem no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        if item.devuelto:
            return Response({"error": "Este ítem ya fue devuelto."}, status=status.HTTP_400_BAD_REQUEST)

        cantidad = int(request.data.get("cantidad", item.cantidad_recibida))
        if cantidad <= 0:
            return Response({"error": "La cantidad a devolver debe ser mayor a cero."}, status=status.HTTP_400_BAD_REQUEST)
        disponible = int(item.cantidad_recibida - item.cantidad_devuelta)
        if cantidad > disponible:
            return Response({"error": f"La cantidad supera lo recibido. Disponible para devolver: {disponible}."}, status=status.HTTP_400_BAD_REQUEST)

        username = resolve_username(request)
        traslado = _crear_traslado_enviado(
            solicitud.bodega_destino,
            solicitud.bodega_origen,
            [
                {
                    "sku": item.sku,
                    "descripcion": item.descripcion,
                    "cantidad": cantidad,
                }
            ],
            username or "Sistema",
            departamento=request.data.get("departamento"),
            entregamos_a=request.data.get("entregamos_a"),
        )

        item.cantidad_devuelta = item.cantidad_devuelta + cantidad
        if item.cantidad_devuelta >= item.cantidad_recibida:
            item.devuelto = True
        item.traslado_devolucion = traslado
        item.devuelto_en = timezone.now()
        item.devuelto_por = username
        item.usuario_traslado_devolucion = request.data.get("entregamos_a")
        item.departamento_traslado_devolucion = request.data.get("departamento")
        item.save(
            update_fields=[
                "cantidad_devuelta",
                "devuelto",
                "traslado_devolucion",
                "devuelto_en",
                "devuelto_por",
                "usuario_traslado_devolucion",
                "departamento_traslado_devolucion",
                "actualizado_en",
            ]
        )

        return Response(self.get_serializer(solicitud).data)


class IngestaExcretaViewSet(AdmisionScopedViewSet):
    queryset = IngestaExcretaDia.objects.all().order_by("-fecha", "-creado_en")
    serializer_class = IngestaExcretaDiaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("registros")

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.instance.ensure_registros()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        serializer.instance.ensure_registros()


class ControlMedicamentoRegistroViewSet(viewsets.ModelViewSet):
    queryset = ControlMedicamentoRegistro.objects.all().order_by("-registrado_en")
    serializer_class = ControlMedicamentoRegistroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        control_id = self.request.query_params.get("control")
        if control_id:
            queryset = queryset.filter(control=control_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(registrado_por=resolve_username(self.request))

    def perform_update(self, serializer):
        serializer.save()


class OrdenMedicaViewSet(AdmisionScopedViewSet):
    queryset = OrdenMedica.objects.all().order_by("-creado_en")
    serializer_class = OrdenMedicaSerializer

    @action(detail=True, methods=["post"], url_path="evento")
    def crear_evento(self, request, pk=None):
        orden = self.get_object()
        data = request.data.copy()
        data["orden"] = orden.pk
        serializer = OrdenMedicaEventoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creado_por=resolve_username(request))

        # Actualizar estado de la orden si viene en el payload
        nuevo_estado = serializer.validated_data.get("estado")
        if nuevo_estado and orden.estado != nuevo_estado:
            orden.estado = nuevo_estado
            if nuevo_estado == "FINALIZADA":
                orden.cerrado_por = resolve_username(request)
                orden.cerrado_en = serializer.instance.creado_en
            orden.save(update_fields=["estado", "cerrado_por", "cerrado_en"])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdenMedicaEventoViewSet(viewsets.ModelViewSet):
    queryset = OrdenMedicaEvento.objects.all().order_by("-creado_en")
    serializer_class = OrdenMedicaEventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        orden_id = self.request.query_params.get("orden")
        if orden_id:
            queryset = queryset.filter(orden=orden_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creado_por=resolve_username(self.request))


class NotaEnfermeriaViewSet(AdmisionScopedViewSet):
    queryset = NotaEnfermeria.objects.all().order_by("-creado_en")
    serializer_class = NotaEnfermeriaSerializer


def _user_roles(user):
    if not user or not user.is_authenticated:
        return []
    roles_manager = getattr(user, "roles", None)
    if roles_manager is None:
        return []
    return [role.name.upper() for role in roles_manager.all()]


def _user_is_doctor(user):
    if not user or not user.is_authenticated:
        return False
    perfil = getattr(user, "perfil", None)
    if getattr(perfil, "es_medico", False):
        return True
    role_names = _user_roles(user)
    return any("MEDICO" in name or "MÉDICO" in name or "DOCTOR" in name for name in role_names)


def _build_doctor_metadata(request):
    username = resolve_username(request)
    full_name = None
    colegiado = None
    user = request.user if request.user.is_authenticated else None
    if user:
        full_name = user.get_full_name().strip() or None
        perfil = getattr(user, "perfil", None)
        if perfil:
            if not full_name:
                nombres = [
                    perfil.primer_nombre,
                    perfil.segundo_nombre,
                    perfil.primer_apellido,
                    perfil.segundo_apellido,
                ]
                full_name = " ".join(filter(None, nombres)).strip() or None
            colegiado = perfil.colegiado or None
    if not full_name:
        full_name = request.headers.get("X-User-Name") or username
    colegiado = colegiado or request.headers.get("X-User-Colegiado")
    return username, full_name, colegiado


def _normalize_identifier(value):
    if not value:
        return ""
    return str(value).strip().lower()


class EvolucionClinicaViewSet(AdmisionScopedViewSet):
    queryset = EvolucionClinica.objects.all().order_by("-creado_en")
    serializer_class = EvolucionClinicaSerializer

    def _ensure_doctor(self):
        if not _user_is_doctor(self.request.user):
            raise PermissionDenied("Solo los médicos pueden gestionar evoluciones clínicas.")

    def perform_create(self, serializer):
        self._ensure_doctor()
        username, nombre, colegiado = _build_doctor_metadata(self.request)
        serializer.save(
            creado_por_username=username,
            actualizado_por_username=username,
            medico_nombre=nombre,
            medico_colegiado=colegiado,
        )

    def perform_update(self, serializer):
        instance = serializer.instance
        username = resolve_username(self.request)
        if instance.creado_por_username:
            if _normalize_identifier(instance.creado_por_username) != _normalize_identifier(username):
                raise PermissionDenied("Solo el médico que registró la evolución puede editarla.")
        self._ensure_doctor()
        _, nombre, colegiado = _build_doctor_metadata(self.request)
        serializer.save(
            actualizado_por_username=username,
            medico_nombre=nombre or instance.medico_nombre,
            medico_colegiado=colegiado or instance.medico_colegiado,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = resolve_username(request)
        if instance.creado_por_username and _normalize_identifier(instance.creado_por_username) != _normalize_identifier(username):
            raise PermissionDenied("Solo el médico que registró la evolución puede eliminarla.")
        self._ensure_doctor()
        return super().destroy(request, *args, **kwargs)


class RegistroDietaViewSet(AdmisionScopedViewSet):
    queryset = RegistroDieta.objects.all().order_by("-registrado_en")
    serializer_class = RegistroDietaSerializer
