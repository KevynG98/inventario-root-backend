"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.urls import path, include, re_path
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework import permissions
from drf_yasg.views import get_schema_view  # type: ignore
from drf_yasg import openapi  # type: ignore

from .path import inventarioUrl, userUrl, rolUrl, proyectosUrl
from .views.emailTestView import correo_prueba


def get_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


schema_view = get_schema_view(
    openapi.Info(
        title="API Inventario General",
        default_version='v1',
        description="Documentación del sistema Inventario General",
        contact=openapi.Contact(email="soporte@ejemplo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', lambda request: redirect('schema-swagger-ui', permanent=False)),
    path('csrf/', get_csrf, name='csrf'),
    path('user/', include(userUrl)),
    path('rol/', include(rolUrl)),
    path('inventario/', include(inventarioUrl)),
    path('proyecto/', include(proyectosUrl)),
    path('correo-prueba/', correo_prueba, name='correo_prueba'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
