from django.urls import path
from ..views.inventoryMovementsViews import *

urlpatterns = [
    path('', list_inventory_movements),
    path('create/', create_inventory_movement),
    path('<int:movement_id>/', get_inventory_movement),
    path('<int:movement_id>/update/', update_inventory_movement),
    path('<int:movement_id>/delete/', delete_inventory_movement),
]
