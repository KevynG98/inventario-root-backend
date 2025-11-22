from django.urls import path
from ..views.proyectoCotizacionViews import (
    crear_cotizacion,
    listar_productos_por_proyecto,
    listar_cotizaciones
    
)

urlpatterns = [
    path('cotizaciones/', listar_cotizaciones, name='listar_cotizaciones'),
    path('proyectos-crear/', crear_cotizacion, name='crear_cotizacion'),
    path('listar-productos/<int:proyecto_id>/', listar_productos_por_proyecto, name='listar_productos_por_proyecto'),
    

]
