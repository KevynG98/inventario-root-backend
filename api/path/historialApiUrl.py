from django.urls import path
from ..views.historialApiView import *

urlpatterns = [
    # Listar historial de API
    path('historial-api/', listar_historial_api, name='listar_historial_api'),
    
    # Exportar historial de API a PDF
    path('historial-exportar-pdf/', exportar_historial_pdf, name='exportar_historial_pdf'),
    path('usuarios-exportar-pdf/', exportar_usuarios_pdf, name='exportar_historial_pdf'),
    path('inventario-exportar-pdf/', exportar_skus_pdf, name='exportar_historial_pdf'),
]
