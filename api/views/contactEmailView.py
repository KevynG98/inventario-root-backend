from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.utils.email_utils import enviar_correo_html


def enviar_correo_nueva_cotizacion(*, nombre_empresa: str, email_empresa: str, telefono_empresa: str, direccion: str, productos: list | None = None) -> None:
    """Envía un correo al mismo destinatario de ``enviar_contacto`` avisando de una nueva cotización.

    ``productos`` debe ser una lista de diccionarios con las llaves:
    - "nombre": nombre del producto
    - "cantidad": cantidad solicitada
    """
    destinatario = settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
    if not destinatario:
        # Si no hay destinatario configurado, no intentamos enviar correo
        return

    asunto = "Nueva cotización"

    productos = productos or []

    texto_plano = (
        "Se ha registrado una nueva cotización:\n\n"
        f"Nombre de la empresa: {nombre_empresa}\n"
        f"Email de la empresa: {email_empresa}\n"
        f"Teléfono de la empresa: {telefono_empresa}\n"
        f"Dirección de la empresa: {direccion}\n\n"
    )

    if productos:
        texto_plano += "Productos solicitados:\n"
        for p in productos:
            texto_plano += f"- {p.get('nombre', '')}: {p.get('cantidad', '')}\n"

    # HTML para listado de productos
    productos_html_rows = ""
    for p in productos:
        nombre = p.get("nombre", "")
        cantidad = p.get("cantidad", "")
        productos_html_rows += f"""
                          <tr>
                            <td style=\"padding:6px 8px;color:#455a64;font-size:13px;border-bottom:1px solid #eceff1;\">{nombre}</td>
                            <td style=\"padding:6px 8px;color:#263238;font-weight:600;font-size:13px;text-align:center;border-bottom:1px solid #eceff1;\">{cantidad}</td>
                          </tr>
        """

    productos_section_html = ""
    if productos_html_rows:
        productos_section_html = f"""
                        <p style=\"margin:24px 0 8px;color:#37474f;font-size:14px;font-weight:600;\">Productos solicitados</p>
                        <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"border-collapse:collapse;font-size:14px;background-color:#fafbfc;border-radius:6px;overflow:hidden;\">
                          <thead>
                            <tr style=\"background-color:#eceff1;\">
                              <th align=\"left\" style=\"padding:8px 8px;color:#607d8b;font-size:12px;text-transform:uppercase;letter-spacing:0.03em;\">Producto</th>
                              <th align=\"center\" style=\"padding:8px 8px;color:#607d8b;font-size:12px;text-transform:uppercase;letter-spacing:0.03em;\">Cantidad</th>
                            </tr>
                          </thead>
                          <tbody>
        {productos_html_rows}
                          </tbody>
                        </table>
        """

    html = f"""
        <html>
          <body style="margin:0;padding:0;background-color:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8;padding:20px 0;">
              <tr>
                <td align="center">
                  <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                    <tr>
                      <td style="background:linear-gradient(90deg,#0d47a1,#1976d2);padding:20px 24px;color:#ffffff;">
                        <h1 style="margin:0;font-size:22px;font-weight:600;">Nueva cotización</h1>
                        <p style="margin:4px 0 0;font-size:14px;opacity:0.9;">Se ha registrado una nueva solicitud de cotización.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:24px;background-color:#ffffff;">
                        <p style="margin:0 0 16px;color:#37474f;font-size:14px;">Hola,</p>
                        <p style="margin:0 0 16px;color:#455a64;font-size:14px;">
                          Se ha creado una nueva cotización con la siguiente información de la empresa:
                        </p>
                        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:14px;">
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;width:180px;">Nombre de la empresa:</td>
                            <td style="padding:8px 0;color:#263238;font-weight:600;">{nombre_empresa}</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;">Email de la empresa:</td>
                            <td style="padding:8px 0;color:#1976d2;font-weight:600;">{email_empresa}</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;">Teléfono de la empresa:</td>
                            <td style="padding:8px 0;color:#263238;font-weight:600;">{telefono_empresa}</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;">Dirección de la empresa:</td>
                            <td style="padding:8px 0;color:#263238;font-weight:600;">{direccion}</td>
                          </tr>
                        </table>
        {productos_section_html}
                        <p style="margin:24px 0 0;color:#78909c;font-size:12px;">
                          Te recomendamos dar seguimiento a esta cotización a la brevedad.
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="background-color:#eceff1;padding:12px 24px;text-align:center;color:#90a4ae;font-size:11px;">
                        Este es un mensaje automático relacionado con nuevas cotizaciones.
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
    """

    enviar_correo_html(
        asunto=asunto,
        destinatarios=[destinatario],
        texto_plano=texto_plano,
        html=html,
    )


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
