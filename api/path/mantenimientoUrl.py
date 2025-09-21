from django.urls import path
from ..views.mantenimientoViews import (
    listar_centros_costo, crear_centro_costo, actualizar_centro_costo, eliminar_centro_costo, obtener_centro_costo,
    listar_departamentos, crear_departamento, actualizar_departamento, eliminar_departamento, obtener_departamento,
    listar_cuentas_contables, crear_cuenta_contable, actualizar_cuenta_contable, eliminar_cuenta_contable, obtener_cuenta_contable,
)
from ..views.cargaMasivaViews import (
    listar_cargas_existencias,
    detalle_carga_existencias,
    crear_carga_existencias,
    listar_cargas_precios,
    detalle_carga_precios,
    crear_carga_precios,
)

urlpatterns = [
    # Centros de Costo
    path('centros-costo/', listar_centros_costo, name='listar_centros_costo'),
    path('centros-costo/crear/', crear_centro_costo, name='crear_centro_costo'),
    path('centros-costo/actualizar/<int:pk>/', actualizar_centro_costo, name='actualizar_centro_costo'),
    path('centros-costo/eliminar/<int:pk>/', eliminar_centro_costo, name='eliminar_centro_costo'),
    path('centros-costo/<int:pk>/', obtener_centro_costo, name='obtener_centro_costo'),

    # Departamentos
    path('departamentos/', listar_departamentos, name='listar_departamentos'),
    path('departamentos/crear/', crear_departamento, name='crear_departamento'),
    path('departamentos/actualizar/<int:pk>/', actualizar_departamento, name='actualizar_departamento'),
    path('departamentos/eliminar/<int:pk>/', eliminar_departamento, name='eliminar_departamento'),
    path('departamentos/<int:pk>/', obtener_departamento, name='obtener_departamento'),

    # Cuentas Contables
    path('cuentas-contables/', listar_cuentas_contables, name='listar_cuentas_contables'),
    path('cuentas-contables/crear/', crear_cuenta_contable, name='crear_cuenta_contable'),
    path('cuentas-contables/actualizar/<int:pk>/', actualizar_cuenta_contable, name='actualizar_cuenta_contable'),
    path('cuentas-contables/eliminar/<int:pk>/', eliminar_cuenta_contable, name='eliminar_cuenta_contable'),
    path('cuentas-contables/<int:pk>/', obtener_cuenta_contable, name='obtener_cuenta_contable'),

    # Carga masiva existencias
    path('carga-masiva/existencias/', listar_cargas_existencias, name='listar_cargas_existencias'),
    path('carga-masiva/existencias/<int:pk>/', detalle_carga_existencias, name='detalle_carga_existencias'),
    path('carga-masiva/existencias/crear/', crear_carga_existencias, name='crear_carga_existencias'),

    # Carga masiva precios
    path('carga-masiva/precios/', listar_cargas_precios, name='listar_cargas_precios'),
    path('carga-masiva/precios/<int:pk>/', detalle_carga_precios, name='detalle_carga_precios'),
    path('carga-masiva/precios/crear/', crear_carga_precios, name='crear_carga_precios'),
]
