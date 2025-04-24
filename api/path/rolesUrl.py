from django.urls import path
from ..views.rolesViews import list_roles, assign_role, create_role

urlpatterns = [
    path('', list_roles),
    path('assign/', assign_role),
    path('create/', create_role)
]
