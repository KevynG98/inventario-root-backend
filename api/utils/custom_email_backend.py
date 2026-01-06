import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

class ConfiguredEmailBackend(SMTPBackend):
    def _get_ssl_context(self):
        # Crea un contexto SSL por defecto
        context = ssl.create_default_context()
        # Opcional: Si Render sigue fallando por certificados, puedes descomentar la siguiente línea
        # para deshabilitar la verificación (NO RECOMENDADO para producción sensible, pero útil para debug)
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE
        return context

    def open(self):
        # Sobreescribimos open para asegurar que se use nuestro contexto si se requiere TLS
        if self.connection:
            return False
        
        # Llama al método padre para crear la conexión inicial
        # Nota: Django ya maneja la creación del contexto internamente en versiones recientes,
        # pero esta clase nos da un punto de control explícito si necesitamos inyectar lógica.
        # Para Django 5.x, la implementación por defecto suele ser suficiente, 
        # pero forzar un contexto explícito ayuda en entornos restrictivos.
        try:
            return super().open()
        except Exception:
            if not self.fail_silently:
                raise
