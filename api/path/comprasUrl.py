from django.urls import path
from ..views.comprasViews import (
    listar_requisiciones_autorizadas,
    listar_ordenes_compra,
    crear_oc_desde_requisicion,
    obtener_orden_compra,
    editar_orden_compra,
    anular_orden_compra,
    generar_orden_compra,
    descargar_pdf_orden_compra,
)

urlpatterns = [
    # Requisiciones autorizadas para orden de compra
    path('requisiciones/', listar_requisiciones_autorizadas),

    # Ordenes de compra
    path('ordenes-compra/', listar_ordenes_compra),
    path('ordenes-compra/crear-desde-requisicion/<int:requisicion_id>/', crear_oc_desde_requisicion),
    path('ordenes-compra/<int:id>/', obtener_orden_compra),
    path('ordenes-compra/<int:id>/editar/', editar_orden_compra),
    path('ordenes-compra/<int:id>/anular/', anular_orden_compra),
    path('ordenes-compra/<int:id>/generar/', generar_orden_compra),
    path('ordenes-compra/<int:id>/pdf/', descargar_pdf_orden_compra),
]
