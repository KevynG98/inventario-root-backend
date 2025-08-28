from django.urls import path
from ..views.entradasViews import (
    listar_entradas, crear_entrada, obtener_entrada, aplicar_entrada,
    actualizar_entrada, eliminar_entrada,
)
from ..views.salidasViews import (
    listar_salidas, crear_salida, obtener_salida,
)
from ..views.trasladosViews import (
    listar_traslados, crear_traslado, obtener_traslado, recibir_traslado, anular_traslado,
)

bodegasUrl = ([
    # Entradas
    path('entradas/', listar_entradas, name='listar_entradas'),
    path('entradas/crear/', crear_entrada, name='crear_entrada'),
    path('entradas/<int:pk>/', obtener_entrada, name='obtener_entrada'),
    path('entradas/aplicar/<int:pk>/', aplicar_entrada, name='aplicar_entrada'),
    path('entradas/actualizar/<int:pk>/', actualizar_entrada, name='actualizar_entrada'),
    path('entradas/eliminar/<int:pk>/', eliminar_entrada, name='eliminar_entrada'),

    # Salidas
    path('salidas/', listar_salidas, name='listar_salidas'),
    path('salidas/crear/', crear_salida, name='crear_salida'),
    path('salidas/<int:pk>/', obtener_salida, name='obtener_salida'),

    # Traslados
    path('traslados/', listar_traslados, name='listar_traslados'),
    path('traslados/crear/', crear_traslado, name='crear_traslado'),
    path('traslados/<int:pk>/', obtener_traslado, name='obtener_traslado'),
    path('traslados/<int:pk>/recibir/', recibir_traslado, name='recibir_traslado'),
    path('traslados/<int:pk>/anular/', anular_traslado, name='anular_traslado'),
], 'bodegas')
