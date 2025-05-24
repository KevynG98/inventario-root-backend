from django.urls import path
from ..views.inventarioProveedoresViews import (
    listar_proveedores,
    crear_proveedor,
    actualizar_proveedor,
    eliminar_proveedor,
    obtener_proveedor,
    eliminar_proveedor
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
    
]
