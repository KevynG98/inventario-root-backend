from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.utils.email_utils import enviar_correo_html


@api_view(["POST"])
@permission_classes([AllowAny])
def enviar_contacto(request):
    """
    Recibe datos del formulario de contacto y envía un correo al remitente configurado.
    Espera JSON con: nombre, email, mensaje.
    """
    data = request.data or {}
    nombre = (data.get("nombre") or "").strip()
    email = (data.get("email") or "").strip()
    mensaje = (data.get("mensaje") or "").strip()

    if not nombre or not email or not mensaje:
        return Response(
            {"detail": "nombre, email y mensaje son obligatorios."}, status=400
        )

    destinatario = settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
    if not destinatario:
        return Response(
            {"detail": "Configura EMAIL_HOST_USER en tu .env para recibir los contactos."},
            status=500,
        )

    texto_plano = (
        f"Nuevo mensaje desde la landing:\n"
        f"Nombre: {nombre}\n"
        f"Correo: {email}\n\n"
        f"Mensaje:\n{mensaje}"
    )
    html = f"""
        <p><strong>Nuevo mensaje desde la landing</strong></p>
        <p><strong>Nombre:</strong> {nombre}</p>
        <p><strong>Correo:</strong> {email}</p>
        <p><strong>Mensaje:</strong><br>{mensaje.replace('\n', '<br>')}</p>
    """

    try:
        enviar_correo_html(
            asunto="Nuevo mensaje de contacto - Landing",
            destinatarios=[destinatario],
            texto_plano=texto_plano,
            html=html,
        )
    except Exception as exc:  # pragma: no cover - logging de error simple
        return Response(
            {"detail": "No se pudo enviar el correo de contacto.", "error": str(exc)},
            status=500,
        )

    return Response({"detail": "Mensaje enviado correctamente."})
