from django.urls import path
from ..views.inventoryViews import *

urlpatterns = [
    path('', list_inventory),
    path('avariable/', available_inventory),
    path('create/', create_inventory),
    path('<int:pk>/', retrieve_inventory),
    path('<int:pk>/update/', update_inventory),
    path('<int:pk>/delete/', mark_inventory_as_used),
]
