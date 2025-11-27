from django.urls import path
from ..views.proyectoCotizacionViews import (
    crear_cotizacion,
    listar_productos_por_proyecto,
    listar_cotizaciones,
    cotización_cancelada,
    cotizacion_aprobada,
    listar_cotizaciones_rechazadas
)

from ..views.proyectoManagementViews import (
    listar_pryectos,
    actualizar_estatus_proyecto
)

urlpatterns = [
    path('cotizaciones/', listar_cotizaciones, name='listar_cotizaciones'),
    path('proyectos-crear/', crear_cotizacion, name='crear_cotizacion'),
    path('listar-productos/<int:proyecto_id>/', listar_productos_por_proyecto, name='listar_productos_por_proyecto'),
    path('proyectos/rechaza-cotizacion', cotización_cancelada, name='rechaza_cotizacion'), 
    path('aprueba-cotizacion', cotizacion_aprobada, name='aprueba_cotizacion'),
    path('cotizaciones-rechazadas/', listar_cotizaciones_rechazadas, name='listar_cotizaciones_rechazadas'),
    
    path('', listar_pryectos, name='listar_pryectos'),
    path('actualizar-estatus', actualizar_estatus_proyecto, name='actualizar_estatus_proyecto'),
]
