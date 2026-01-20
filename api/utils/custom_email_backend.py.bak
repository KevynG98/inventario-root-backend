import ssl
import socket
import time
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
        
        print(f"⏱️ [EMAIL TIMING] Iniciando conexión SMTP a {self.host}:{self.port}...")
        start_time = time.time()

        # --- PARCHE IPv4 ---
        # Render y otros hostings a veces fallan con IPv6 (Errno 101).
        # Forzamos momentáneamente la resolución DNS a IPv4.
        original_getaddrinfo = socket.getaddrinfo

        def ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            # Si se pide familia no especificada (0) o IPv6, forzamos IPv4 (AF_INET)
            dns_start = time.time()
            if family == 0 or family == socket.AF_INET6:
                family = socket.AF_INET
            
            res = original_getaddrinfo(host, port, family, type, proto, flags)
            dns_end = time.time()
            print(f"⏱️ [EMAIL TIMING] DNS Resolution ({host}) took {dns_end - dns_start:.4f}s")
            return res

        socket.getaddrinfo = ipv4_getaddrinfo
        # -------------------

        try:
            print(f"⏱️ [EMAIL TIMING] Llamando a super().open()...")
            result = super().open()
            end_time = time.time()
            print(f"⏱️ [EMAIL TIMING] Conexión establecida exitosamente en {end_time - start_time:.4f}s")
            return result
        except Exception as e:
            end_time = time.time()
            print(f"❌ [EMAIL ERROR] Falló conexión tras {end_time - start_time:.4f}s. Error: {e}")

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
