from django.urls import path
from ..views.purchaseOrderDetailViews import *

urlpatterns = [
    path('', list_purchase_order_details),
    path('create/', create_purchase_order_detail),
    path('<int:pk>/', retrieve_purchase_order_detail),
    path('<int:pk>/update/', update_purchase_order_detail),
    path('<int:pk>/delete/', delete_purchase_order_detail),
]
