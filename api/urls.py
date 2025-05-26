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
    inventarioUrl, userUrl, rolesUrl, customerUrl, utilsUrl,
    admisionesUrl, habitacionesUrl
)

def get_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

urlpatterns = [
    path('csrf/', get_csrf, name='csrf'),
    # path('admin/', admin.site.urls),
    path('user/', include(userUrl)),
    path('rol/', include(rolesUrl)),
    path('admisiones/', include(admisionesUrl)),
    path('habitaciones/', include(habitacionesUrl)),
    path('inventario/', include(inventarioUrl)),
    # path('customer/', include(customerUrl)),
    path('utils/', include(utilsUrl)),
]
