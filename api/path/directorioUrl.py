from django.urls import path
from ..views.directorioViewa import *

urlpatterns = [
    #Directorio CRUD
    path('', listar_directorio, name='listar_directorio'),
    path('crear/', crear_directorio, name='crear_directorio'),
    path('actualizar/<int:pk>/', actualizar_directorio, name='actualizar_directorio'),
    path('eliminar/<int:pk>/', eliminar_directorio, name='eliminar_directorio'),
    path('<int:pk>/', obtener_directorio, name='obtener_directorio'),
]