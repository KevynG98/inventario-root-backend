from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

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
)
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
)


def resolve_username(request):
    if request.user and request.user.is_authenticated:
        return request.user.username
    return request.headers.get("X-User")


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
