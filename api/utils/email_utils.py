import logging
from typing import List
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_correo_basico(asunto: str, mensaje: str, destinatarios: List[str]) -> int:
    """
    Envía un correo de texto plano de forma segura.
    Retorna 1 si se envió, 0 si falló, pero NO levanta excepción.
    """
    try:
        return send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=destinatarios,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"❌ Error enviando correo básico a {destinatarios}: {str(e)}")
        return 0


def enviar_correo_html(
    asunto: str,
    destinatarios: List[str],
    texto_plano: str,
    html: str,
) -> None:
    """
    Envía un correo HTML de forma segura.
    Captura excepciones para no romper el request HTTP.
    """
    try:
        email = EmailMultiAlternatives(
            subject=asunto,
            body=texto_plano,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=destinatarios,
        )
        email.attach_alternative(html, "text/html")
        email.send(fail_silently=False)
    except Exception as e:
        logger.error(f"❌ Error enviando correo HTML a {destinatarios}: {str(e)}")

