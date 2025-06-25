from django.urls import path
from ..views.admisionesViews import (
    crear_admision,
    obtener_admision,
    listar_admisiones_por_area,
    resumen_admisiones_por_area,
    listar_admisiones_resumen,
    editar_admision,
    ListadoAdmisionesView,
    listar_admisiones_estado,
    estado_cuenta,
    crear_movimiento,
    generar_estado_cuenta_pdf
)

urlpatterns = [
    path('', crear_admision, name='crear_admision'),
    path('<int:admision_id>/', obtener_admision, name='obtener_admision'),
    path('editar/<int:pk>/', editar_admision, name='editar_admision'),
    path('all/', ListadoAdmisionesView.as_view(), name='listar_admisiones'),

    # Extras
    path('admisiones-por-area/', listar_admisiones_por_area, name='listar_admisiones_por_area'),
    path('admisiones-resumen-por-area/', resumen_admisiones_por_area, name='resumen_admisiones_por_area'),
    path('admisiones-resumen/', listar_admisiones_resumen, name='listar_admisiones_resumen'),
    path('admisiones-resumen-estado/', listar_admisiones_estado, name='listar_admisiones_estado'),
    
    # Estado de cuentas
    path('estado-cuenta/<int:admision_id>/', estado_cuenta, name='estado-cuenta'),
    path('movimientos-crear/', crear_movimiento, name='crear-movimiento'),
    path('estado-cuenta-imprimir/<int:admision_id>/', generar_estado_cuenta_pdf),
]
