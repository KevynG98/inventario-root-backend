from django.urls import path
from ..views.salesDetailViewa import *

urlpatterns = [
    path('', list_sale_details),
    path('create/', create_sale_detail),
    path('<int:pk>/', retrieve_sale_detail),
    path('<int:pk>/update/', update_sale_detail),
    path('<int:pk>/delete/', delete_sale_detail),
]
