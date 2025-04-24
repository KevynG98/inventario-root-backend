from django.urls import path
from ..views.productViews import *

urlpatterns = [
    path('', list_products, name='list_products'),
    path('create/', create_product, name='create_product'),
    path('/<int:pk>', retrieve_product, name='retrieve_product'),
    path('update/<int:pk>/', update_product, name='update_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]
