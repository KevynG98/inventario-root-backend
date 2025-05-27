from django.urls import path
from ..views.historialApiView import listar_historial_api

urlpatterns = [
    path('historial-api/', listar_historial_api, name='listar_historial_api'),
]
