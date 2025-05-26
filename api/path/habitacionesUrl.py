from django.urls import path
from ..views.habitacionesViews import (
    listar_habitaciones,
    crear_habitacion,
    listar_all_habitaciones,
    obtener_habitacion,
    actualizar_habitacion,
    eliminar_habitacion
)

urlpatterns = [
    path('', listar_all_habitaciones, name='listar_all_habitaciones'),
    path('habitaciones-listar/', listar_habitaciones, name='listar_habitaciones'),
    path('habitaciones-crear/', crear_habitacion, name='crear_habitacion'),
    path('<int:pk>/', obtener_habitacion, name='obtener_habitacion'),
    path('habitaciones-actualizar/<int:pk>/', actualizar_habitacion, name='actualizar_habitacion'),
    path('habitaciones-eliminar/<int:pk>/', eliminar_habitacion, name='eliminar_habitacion'),
]