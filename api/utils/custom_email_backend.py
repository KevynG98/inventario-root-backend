import ssl
import socket
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

class ConfiguredEmailBackend(SMTPBackend):
    def _get_ssl_context(self):
        # Crea un contexto SSL por defecto
        context = ssl.create_default_context()
        # En entornos como Render/Vercel, a veces la resolución DNS reversa falla 
        # y causa delays. Relajamos esto para ganar velocidad.
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def open(self):
        # Sobreescribimos open para asegurar que se use nuestro contexto si se requiere TLS
        if self.connection:
            return False
        
        # --- PARCHE IPv4 ---
        # Render y otros hostings a veces fallan con IPv6 (Errno 101).
        # Forzamos momentáneamente la resolución DNS a IPv4.
        original_getaddrinfo = socket.getaddrinfo

        def ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            # Si se pide familia no especificada (0) o IPv6, forzamos IPv4 (AF_INET)
            if family == 0 or family == socket.AF_INET6:
                family = socket.AF_INET
            return original_getaddrinfo(host, port, family, type, proto, flags)

        socket.getaddrinfo = ipv4_getaddrinfo
        # -------------------

        try:
            return super().open()
        except Exception as e:
            # DIAGNÓSTICO: Si falla por Network Unreachable (101), imprimimos info de resolución
            if isinstance(e, OSError) and getattr(e, 'errno', None) == 101:
                print(f"❌ [EMAIL ERROR] Network unreachable connecting to {self.host}:{self.port}")
                try:
                    # Usamos el original para ver qué estaba pasando realmente
                    socket.getaddrinfo = original_getaddrinfo 
                    infos = socket.getaddrinfo(self.host, self.port, proto=socket.IPPROTO_TCP)
                    print(f"🔍 DNS Resolution for {self.host}: {infos}")
                except Exception as dns_err:
                    print(f"⚠️ Could not resolve DNS during error handling: {dns_err}")
            
            if not self.fail_silently:
                raise
        finally:
            # Restauramos siempre el comportamiento original del socket
            socket.getaddrinfo = original_getaddrinfo
