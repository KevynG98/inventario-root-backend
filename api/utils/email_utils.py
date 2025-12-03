from typing import List

from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings


def enviar_correo_basico(asunto: str, mensaje: str, destinatarios: List[str]) -> int:
    """
    Envía un correo de texto plano usando la configuración SMTP definida en settings.py.
    Define EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER y EMAIL_HOST_PASSWORD en tu .env.
    """
    return send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=False,
    )


def enviar_correo_html(
    asunto: str,
    destinatarios: List[str],
    texto_plano: str,
    html: str,
) -> None:
    """
    Envía un correo con versión texto y HTML.
    Usa las mismas variables de entorno de SMTP que enviar_correo_basico.
    """
    email = EmailMultiAlternatives(
        subject=asunto,
        body=texto_plano,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios,
    )
    email.attach_alternative(html, "text/html")
    email.send(fail_silently=False)
