from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.utils.email_utils import enviar_correo_basico


@api_view(["GET"])
@permission_classes([AllowAny])
def correo_prueba(request):
    """
    Endpoint de prueba para envío de correo SMTP.
    Usa las variables EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER y EMAIL_HOST_PASSWORD definidas en .env.
    Puedes pasar ?to=correo@destino.com, de lo contrario usa EMAIL_HOST_USER como destinatario.
    """
    destinatario = request.query_params.get("to")
    if not destinatario:
        from django.conf import settings

        if not settings.EMAIL_HOST_USER:
            return Response(
                {"detail": "Configura EMAIL_HOST_USER o envía ?to=correo@destino.com"},
                status=400,
            )
        destinatario = settings.EMAIL_HOST_USER

    enviar_correo_basico(
        asunto="Prueba de correo desde Inventario General",
        mensaje="Este es un correo de prueba del entorno Django.",
        destinatarios=[destinatario],
    )
    return Response({"detail": f"Correo enviado a {destinatario}"})
