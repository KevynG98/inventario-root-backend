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
from ..views.inventarioMedidaViews import (
    listar_medidas,
    crear_medida,
    actualizar_medida,
    eliminar_medida,
    obtener_medida,
)
from ..views.inventarioCategoriasViews import (
    listar_categorias,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
    obtener_categoria,
)

from ..views.inventarioBodegasViews import (
    listar_bodegas,
    crear_bodegas,
    actualizar_bodegas,
    eliminar_bodegas,
    obtener_bodegas,
)

from ..views.inventarioSkuView import (
    listar_skus, crear_sku, obtener_sku, actualizar_sku, eliminar_sku,
    mover_producto, listar_skus_con_bodegas, detalle_sku_con_bodegas
)

urlpatterns = [
    #proveedores CRUD
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    path('proveedores-crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores-actualizar/<int:pk>/', actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores-eliminar/<int:pk>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/<int:pk>/', obtener_proveedor, name='obtener_proveedor'),
    
    #Marcas CRUD
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas-crear/', crear_marca, name='crear_marca'),
    path('marcas-actualizar/<int:pk>/', actualizar_marca, name='actualizar_marca'),
    path('marcas-eliminar/<int:pk>/', eliminar_marca, name='eliminar_marca'),
    path('marcas/<int:pk>/', obtener_marca, name='obtener_marca'),
    
    #Unidades de medida CRUD
    path('medidas/', listar_medidas, name='listar_medidas'),
    path('medidas-crear/', crear_medida, name='crear_medida'),
    path('medidas-actualizar/<int:pk>/', actualizar_medida, name='actualizar_medida'),
    path('medidas-eliminar/<int:pk>/', eliminar_medida, name='eliminar_medida'),
    path('medidas/<int:pk>/', obtener_medida, name='obtener_medida'),
    
    #Categorias CRUD
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('categorias-crear/', crear_categoria, name='crear_categoria'),
    path('categorias-actualizar/<int:pk>/', actualizar_categoria, name='actualizar_categoria'),
    path('categorias-eliminar/<int:pk>/', eliminar_categoria, name='eliminar_categoria'),
    path('categorias/<int:pk>/', obtener_categoria, name='obtener_categoria'),
    
    #Bodegas CRUD
    path('bodegas/', listar_bodegas, name='listar_bodegas'),
    path('bodegas-crear/', crear_bodegas, name='crear_bodega'),
    path('bodegas-actualizar/<int:pk>/', actualizar_bodegas, name='actualizar_bodega'),
    path('bodegas-eliminar/<int:pk>/', eliminar_bodegas, name='eliminar_bodega'),
    path('bodegas/<int:pk>/', obtener_bodegas, name='obtener_bodega'),
    
    #Inventarios
    path('skus/', listar_skus),
    path('skus-crear/', crear_sku),
    path('skus/<int:pk>/', obtener_sku),
    path('skus-actualizar/<int:pk>/', actualizar_sku),
    path('skus-eliminar/<int:pk>', eliminar_sku),
    path('skus/mover/', mover_producto),
    path('skus-con-bodegas/', listar_skus_con_bodegas),
    path('sku-detalle/<int:pk>/', detalle_sku_con_bodegas, name='sku_con_bodegas_detalle'),

]
