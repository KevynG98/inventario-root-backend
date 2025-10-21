from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.enfermeriaViews import (
    AdmisionMedicoTratanteViewSet,
    AntecedenteClinicoViewSet,
    ControlMedicamentoRegistroViewSet,
    ControlMedicamentoViewSet,
    HistoriaEnfermedadView,
    NotaEnfermeriaViewSet,
    OrdenMedicaEventoViewSet,
    OrdenMedicaViewSet,
    RegistroDietaViewSet,
    SignoVitalEmergenciaViewSet,
    SignoVitalEncamamientoViewSet,
)

router = DefaultRouter()
router.register(r"medicos-tratantes", AdmisionMedicoTratanteViewSet, basename="enfermeria-medicos-tratantes")
router.register(r"signos-vitales-emergencia", SignoVitalEmergenciaViewSet, basename="enfermeria-signos-emergencia")
router.register(r"signos-vitales-encamamiento", SignoVitalEncamamientoViewSet, basename="enfermeria-signos-encamamiento")
router.register(r"antecedentes", AntecedenteClinicoViewSet, basename="enfermeria-antecedentes")
router.register(r"controles-medicamentos", ControlMedicamentoViewSet, basename="enfermeria-controles-medicamentos")
router.register(r"controles-medicamentos-registros", ControlMedicamentoRegistroViewSet, basename="enfermeria-controles-medicamentos-registros")
router.register(r"ordenes-medicas", OrdenMedicaViewSet, basename="enfermeria-ordenes-medicas")
router.register(r"ordenes-medicas-eventos", OrdenMedicaEventoViewSet, basename="enfermeria-ordenes-medicas-eventos")
router.register(r"notas-enfermeria", NotaEnfermeriaViewSet, basename="enfermeria-notas")
router.register(r"dietas", RegistroDietaViewSet, basename="enfermeria-dietas")

urlpatterns = [
    path("", include(router.urls)),
    path("historias-enfermedad/<int:admision_id>/", HistoriaEnfermedadView.as_view(), name="enfermeria-historia-detalle"),
]
