from django.urls import path
from ..views.rolesViews import list_roles, assign_role, create_role, asignar_rol, unassign_role

urlpatterns = [
    path('', list_roles),
    path('assign/', assign_role),
    path('create/', create_role),
    path('rol-cajero/', asignar_rol, name='asignar_rol'),
    path('unassign/', unassign_role, name='asignar_rol'),
]
