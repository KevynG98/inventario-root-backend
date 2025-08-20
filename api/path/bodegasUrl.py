from django.urls import path
from ..views.entradasViews import (
    listar_entradas, crear_entrada, obtener_entrada, aplicar_entrada,
    actualizar_entrada, eliminar_entrada,
)
from ..views.salidasViews import (
    listar_salidas, crear_salida, obtener_salida,
)

bodegasUrl = ([
    # Entradas
    path('entradas/', listar_entradas, name='listar_entradas'),
    path('entradas/crear/', crear_entrada, name='crear_entrada'),
    path('entradas/<int:pk>/', obtener_entrada, name='obtener_entrada'),
    path('entradas/aplicar/<int:pk>/', aplicar_entrada, name='aplicar_entrada'),

    # Salidas
    path('salidas/', listar_salidas, name='listar_salidas'),
    path('salidas/crear/', crear_salida, name='crear_salida'),
    path('salidas/<int:pk>/', obtener_salida, name='obtener_salida'),
], 'bodegas')
