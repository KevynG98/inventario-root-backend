"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .path import (
    userUrl, rolesUrl, productUrl, categoryUrl, supplierUrl, inventoryUrl, 
    inventoryMovementsUrl, purchaseOrderUrl, purchaseOrderDetailUrl, 
    salesPath, salesDetailUrl, customerUrl, recepiesUrl
)

def get_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

urlpatterns = [
    path('csrf/', get_csrf, name='csrf'),
    # path('admin/', admin.site.urls),
    path('user/', include(userUrl)),
    path('rol/', include(rolesUrl)),
    path('products/', include(productUrl)),
    path('category/', include(categoryUrl)),
    # path('supplier/', include(supplierUrl)),
    path('inventory/', include(inventoryUrl)),
    path('inventory-movements/', include(inventoryMovementsUrl)),
    # path('purchase/', include(purchaseOrderUrl)),
    # path('purchase-detail/', include(purchaseOrderDetailUrl)),
    # path('sales/', include(salesPath)),
    # path('sales-detail/', include(salesDetailUrl)),
    # path('customer/', include(customerUrl)),
    path('receta/', include(recepiesUrl)),
]
