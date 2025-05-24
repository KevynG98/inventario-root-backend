from django.urls import path
from ..views.inventarioProveedoresViews import (
    listar_proveedores,
    crear_proveedor,
    actualizar_proveedor,
    eliminar_proveedor,
    obtener_proveedor,
    eliminar_proveedor
)
from ..views.inventarioMarcaViews import (
    listar_marcas,
    crear_marca,
    actualizar_marca,
    eliminar_marca,
    obtener_marca,
)

urlpatterns = [
    #proveedores CRUD
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    path('proveedores-crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores-actualizar/<int:pk>/', actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores-eliminar/<int:pk>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/<int:pk>/', obtener_proveedor, name='obtener_proveedor'),
    path('proveedores-eliminar/<int:pk>/', eliminar_proveedor, name='eliminar_proveedor'),
    
    #Marcas CRUD
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas-crear/', crear_marca, name='crear_marca'),
    path('marcas-actualizar/<int:pk>/', actualizar_marca, name='actualizar_marca'),
    path('marcas-eliminar/<int:pk>/', eliminar_marca, name='eliminar_marca'),
    path('marcas/<int:pk>/', obtener_marca, name='obtener_marca'),
]
