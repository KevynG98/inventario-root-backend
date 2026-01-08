from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import socket
import ssl
from django.conf import settings
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
        if not settings.EMAIL_HOST_USER:
            return Response(
                {"detail": "Configura EMAIL_HOST_USER o envía ?to=correo@destino.com"},
                status=400,
            )
        destinatario = settings.EMAIL_HOST_USER

    # Intento de envío real
    exito = enviar_correo_basico(
        asunto="Prueba de correo desde Inventario General",
        mensaje="Este es un correo de prueba del entorno Django.",
        destinatarios=[destinatario],
    )
    
    msg = f"Correo enviado a {destinatario}" if exito else "Fallo el envío del correo. Revisa logs."
    return Response({"detail": msg, "exito": bool(exito)})


@api_view(["GET"])
@permission_classes([AllowAny])
def diagnostico_red(request):
    """
    Diagnostica la conectividad de red hacia el servidor SMTP.
    """
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    
    results = {
        "host": host,
        "port": port,
        "dns_resolution": [],
        "socket_test": "Pending",
        "error": None
    }
    
    # 1. DNS Resolution
    try:
        # Get all info (IPv4 and IPv6)
        addr_info = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
        results["dns_resolution"] = [str(a) for a in addr_info]
    except Exception as e:
        results["dns_resolution_error"] = str(e)
        return Response(results)

    # 2. Connectivity Test
    log = []
    success = False
    
    for family, type, proto, canonname, sockaddr in addr_info:
        ip = sockaddr[0]
        family_str = "IPv6" if family == socket.AF_INET6 else "IPv4"
        log.append(f"Intentando conectar a {family_str} {ip}:{port}...")
        
        s = None
        try:
            s = socket.socket(family, type, proto)
            s.settimeout(5)
            s.connect(sockaddr)
            log.append(f"✅ Conexión exitosa a {ip}")
            success = True
            
            # Optional: Test SSL handshake if port is 465 or TLS is enabled
            # Just a basic socket connect is enough to prove Network Reachability vs Unreachable
            s.close()
            break 
        except Exception as e:
            log.append(f"❌ Falló conexión a {ip}: {str(e)}")
            if s:
                s.close()

    results["log"] = log
    results["success"] = success
    
    if not success:
         results["socket_test"] = "Failed"
    else:
         results["socket_test"] = "Passed"

    return Response(results)