from django.urls import path
from ..views.productViews import *

urlpatterns = [
    path('', list_products, name='list_products'),
    path('create/', create_product, name='create_product'),
    path('<int:pk>/', retrieve_product, name='retrieve_product'),
    path('<int:pk>/update/', update_product, name='update_product'),
    path('<int:pk>/delete/', delete_product, name='delete_product'),
]
