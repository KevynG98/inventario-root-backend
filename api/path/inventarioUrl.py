from django.urls import path
from ..views.inventarioProveedoresViews import *
from ..views.inventarioMarcaViews import *
from ..views.inventarioMedidaViews import *
from ..views.inventarioCategoriasViews import *
from ..views.inventarioBodegasViews import *
from ..views.inventarioSkuView import *
from ..views.inventarioSegurosView import *
from ..views.inventarioPrecioSkuView import *
from ..views.inventarioPrincipiosView import *
from ..views.movimientosView import listar_movimientos_detalle

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
    path('categorias/subcategorias/<int:categoria_id>/', listar_subcategorias_por_categoria, name='listar_subcategorias_por_categoria'),
    path('subcategorias-crear/', crear_subcategoria, name='crear_subcategoria'),
    
    #Bodegas CRUD
    path('bodegas/', listar_bodegas, name='listar_bodegas'),
    path('bodegas-crear/', crear_bodegas, name='crear_bodega'),
    path('bodegas-actualizar/<int:pk>/', actualizar_bodegas, name='actualizar_bodega'),
    path('bodegas-eliminar/<int:pk>/', eliminar_bodegas, name='eliminar_bodega'),
    path('bodegas/<int:pk>/', obtener_bodegas, name='obtener_bodega'),
    
    #Inventarios
    path('skus/', listar_skus),
    path('skus/buscar/', buscar_skus, name='buscar_skus'),
    path('skus-crear/', crear_sku),
    path('skus/<int:pk>/', obtener_sku),
    path('skus-actualizar/<int:pk>/', actualizar_sku),
    path('skus-eliminar/<int:pk>/', eliminar_sku),
    path('skus/mover/', mover_producto),
    path('skus-con-bodegas/', listar_skus_con_bodegas),
    path('skus-con-bodegas/buscar/', buscar_skus_con_bodegas, name='buscar_skus_con_bodegas'),
    path('sku-detalle/<int:pk>/', detalle_sku_con_bodegas, name='sku_con_bodegas_detalle'),
    path('skus-filtrados/', listar_skus_filtrados, name='listar_skus_filtrados'),
    path('sku-listar/', sku_listar_completo),
    path('movimientos-detalle/', listar_movimientos_detalle),
    
    #Seguros CRUD
    path('seguros/', listar_seguros, name='listar_seguros'),
    path('seguros-crear/', crear_seguros, name='crear_seguros'),
    path('seguros-actualizar/<int:pk>/', actualizar_seguros, name='actualizar_seguros'),
    path('seguros-eliminar/<int:pk>/', eliminar_seguros, name='eliminar_seguros'),
    path('seguros/<int:pk>/', obtener_seguros, name='obtener_seguros'),
    
    #Precio CRUD
    path('precios/', listar_precios),
    path('precios-crear/', crear_precio),
    path('precios-actualizar/<int:pk>/', actualizar_precio),
    path('precios-eliminar/<int:pk>/', eliminar_precio),
    path('precios/buscar/', buscar_precios, name='buscar_precios'),
    
    #Principios Activos CRUD
    path('principios/', listar_principios, name='listar_principios'),
    path('principios-crear/', crear_principios, name='crear_principios'),
    path('principios-actualizar/<int:pk>/', actualizar_principios, name='actualizar_principios'),
    path('principios-eliminar/<int:pk>/', eliminar_principios, name='eliminar_principios'),
    path('principios/<int:pk>/', obtener_principios, name='obtener_principios'),
]
