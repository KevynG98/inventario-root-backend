import logging
import time
from typing import List
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_correo_basico(asunto: str, mensaje: str, destinatarios: List[str]) -> int:
    """
    Envía un correo de texto plano de forma segura con logs de tiempo.
    """
    start = time.time()
    try:
        logger.info(f"⏱️ [UTILS] Iniciando envío básico a {destinatarios}...")
        res = send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=destinatarios,
            fail_silently=False,
        )
        logger.info(f"✅ [UTILS] Envío básico completado en {time.time() - start:.2f}s")
        return res
    except Exception as e:
        logger.error(f"❌ [UTILS] Error tras {time.time() - start:.2f}s enviando a {destinatarios}: {str(e)}")
        return 0


def enviar_correo_html(
    asunto: str,
    destinatarios: List[str],
    texto_plano: str,
    html: str,
) -> None:
    """
    Envía un correo HTML con logs detallados.
    """
    start = time.time()
    try:
        logger.info(f"⏱️ [UTILS] Preparando EmailMultiAlternatives para {destinatarios}...")
        email = EmailMultiAlternatives(
            subject=asunto,
            body=texto_plano,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=destinatarios,
        )
        email.attach_alternative(html, "text/html")
        
        logger.info(f"⏱️ [UTILS] Ejecutando email.send()...")
        email.send(fail_silently=False)
        logger.info(f"✅ [UTILS] Envío HTML completado en {time.time() - start:.2f}s")
    except Exception as e:
        logger.error(f"❌ [UTILS] Error tras {time.time() - start:.2f}s enviando HTML a {destinatarios}: {str(e)}")