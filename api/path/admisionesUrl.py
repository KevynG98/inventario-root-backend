from django.urls import path
from ..views.admisionesViews import (
    crear_admision,
    obtener_admision,
    listar_admisiones_por_area,
    resumen_admisiones_por_area,
    listar_admisiones_resumen,
    editar_admision,
    ListadoAdmisionesView,
    crear_habitacion,
    listar_habitaciones,
    listar_admisiones_estado
)

urlpatterns = [
    path('', crear_admision, name='crear_admision'),
    path('<int:admision_id>/', obtener_admision, name='obtener_admision'),
    path('admisiones-por-area/', listar_admisiones_por_area, name='listar_admisiones_por_area'),
    path('admisiones-resumen-por-area/', resumen_admisiones_por_area, name='resumen_admisiones_por_area'),
    path('admisiones-resumen/', listar_admisiones_resumen, name='listar_admisiones_resumen'),
    path('all/', ListadoAdmisionesView.as_view(), name='listar_admisiones'),
    path('editar/<int:pk>/', editar_admision),
    path('admisiones-resumen-estado/', listar_admisiones_estado),
    #HABITACIONES
    path('habitaciones-listar/', listar_habitaciones, name='Crear habitacion'),
    path('habitaciones-crear/', crear_habitacion, name='crear_habitacion'),
]
