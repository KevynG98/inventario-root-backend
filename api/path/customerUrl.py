from django.urls import path
from ..views.customerViews import *

urlpatterns = [
    path('', list_customers),
    path('create/', create_customer),
    path('<int:pk>/', retrieve_customer),
    path('<int:pk>/update/', update_customer),
    path('<int:pk>/delete/', delete_customer),
]
