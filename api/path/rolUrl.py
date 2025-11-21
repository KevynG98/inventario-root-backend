from django.urls import path
from ..views.rolesView import (
    listar_roles,
    crear_rol,
    asignar_rol,
    desasignar_rol,
)

urlpatterns = [
    path('', listar_roles, name='listar_roles'),
    path('create/', crear_rol, name='crear_rol'),
    path('assign/', asignar_rol, name='asignar_rol'),
    path('unassign/', desasignar_rol, name='desasignar_rol'),
]
