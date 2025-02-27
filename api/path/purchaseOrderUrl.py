from django.urls import path
from ..views.purchaseOrderViews import *

urlpatterns = [
    path('', list_purchase_orders),
    path('create/', create_purchase_order),
    path('<int:order_id>/', get_purchase_order),
    path('<int:order_id>/update/', update_purchase_order),
    path('<int:order_id>/delete/', delete_purchase_order),
]
