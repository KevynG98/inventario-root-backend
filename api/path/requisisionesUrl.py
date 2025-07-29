from django.urls import path
from ..views.requisisionesViews import *

urlpatterns = [
    path('', listar_requisiciones, name='requisicion-list'),
    path('guardar/', guardar_requisicion, name='requisicion-save'),
    path('estado/<int:id>/', cambiar_estado_requisicion, name='requisicion-change-state'),
]
