from django.urls import path
from ..utils.recepiePdf import generar_receta_pdf

urlpatterns = [
    path('recepiepdf/', generar_receta_pdf),
]