from django.urls import path
from ..views.supplierViews import *

urlpatterns = [
    path('', list_suppliers),
    path('create/', create_supplier),
    path('<int:pk>/', retrieve_supplier),
    path('<int:pk>/update/', update_supplier),
    path('<int:pk>/delete/', delete_supplier),
]