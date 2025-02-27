from django.urls import path
from ..views.recepiesViews import *

urlpatterns = [
    path('', listar_recetas, name='listar_recetas'),
    path('crear/', crear_receta, name='crear_receta'),
    path('<int:receta_id>/', obtener_receta, name='obtener_receta'),
    path('<int:receta_id>/procesar/', procesar_receta, name='procesar_receta'),
    path('<int:receta_id>/eliminar/', eliminar_receta, name='eliminar_receta'),
]
