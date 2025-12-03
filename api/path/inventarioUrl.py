from django.urls import path
from ..views.inventarioMarcaViews import (
    listar_marcas,
    crear_marca,
    actualizar_marca,
    eliminar_marca,
    obtener_marca,
)
from ..views.inventarioCategoriasViews import (
    listar_categorias,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
    obtener_categoria,
    listar_subcategorias_por_categoria,
    crear_subcategoria,
    actualizar_subcategoria,
    eliminar_subcategoria,
)
from ..views.inventarioProductosView import (
    listar_productos,
    buscar_productos,
    crear_producto,
    obtener_producto,
    actualizar_producto,
    eliminar_producto,
)
from ..views.inventarioSegurosView import (
    listar_seguros,
    crear_seguros,
    actualizar_seguros,
    eliminar_seguros,
    obtener_seguros,
)
urlpatterns = [
    #Marcas CRUD
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas-crear/', crear_marca, name='crear_marca'),
    path('marcas-actualizar/<int:pk>/', actualizar_marca, name='actualizar_marca'),
    path('marcas-eliminar/<int:pk>/', eliminar_marca, name='eliminar_marca'),
    path('marcas/<int:pk>/', obtener_marca, name='obtener_marca'),
    
    #Categorias CRUD
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('categorias-crear/', crear_categoria, name='crear_categoria'),
    path('categorias-actualizar/<int:pk>/', actualizar_categoria, name='actualizar_categoria'),
    path('categorias-eliminar/<int:pk>/', eliminar_categoria, name='eliminar_categoria'),
    path('categorias/<int:pk>/', obtener_categoria, name='obtener_categoria'),
    path('categorias/subcategorias/<int:categoria_id>/', listar_subcategorias_por_categoria, name='listar_subcategorias_por_categoria'),
    path('subcategorias-crear/', crear_subcategoria, name='crear_subcategoria'),
    path('subcategorias-actualizar/<int:pk>/', actualizar_subcategoria, name='actualizar_subcategoria'),
    path('subcategorias-eliminar/<int:pk>/', eliminar_subcategoria, name='eliminar_subcategoria'),

    #Productos
    path('productos/', listar_productos),
    path('productos/buscar/', buscar_productos, name='buscar_productos'),
    path('productos-crear/', crear_producto),
    path('productos/<int:pk>/', obtener_producto),
    path('productos-actualizar/<int:pk>/', actualizar_producto),
    path('productos-eliminar/<int:pk>/', eliminar_producto),
    
    #Seguros CRUD
    path('seguros/', listar_seguros, name='listar_seguros'),
    path('seguros-crear/', crear_seguros, name='crear_seguros'),
    path('seguros-actualizar/<int:pk>/', actualizar_seguros, name='actualizar_seguros'),
    path('seguros-eliminar/<int:pk>/', eliminar_seguros, name='eliminar_seguros'),
    path('seguros/<int:pk>/', obtener_seguros, name='obtener_seguros'),
]
