from django.urls import path
from ..views.habitacionesViews import (
    listar_habitaciones,
    crear_habitacion,
    listar_all_habitaciones
)

urlpatterns = {
    path('', listar_all_habitaciones, name='listar_all_habitaciones'),
    path('habitaciones-listar/', listar_habitaciones, name='listar_habitaciones'),
    path('habitaciones-crear/', crear_habitacion, name='crear_habitacion'),
}