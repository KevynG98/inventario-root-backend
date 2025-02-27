from django.urls import path
from ..views.salesViews import *

urlpatterns = [
    path('', list_sales),
    path('create/', create_sale),
    path('<int:pk>/', retrieve_sale),
    path('<int:pk>/update/', update_sale),
    path('<int:pk>/delete/', delete_sale),
]
