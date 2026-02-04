from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.utils.email_utils import enviar_correo_html


# URL de la imagen del pie de página para correos de "Nueva cotización".
# Reemplaza este valor por la URL pública donde hospedes la imagen adjunta (flama azul).
FOOTER_GAS_IMAGE_URL = "api/assets/llama-azul-de-la-estufa-en-cocina-concepto-del-gas-y-energía-138429142.webp"

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
            texto_plano += f"- {p.get('nombre', '')}\n"

    # HTML para listado de productos
    productos_html_rows = ""
    for p in productos:
        nombre = p.get("nombre", "")
        # cantidad = p.get("cantidad", "") # Omitido
        productos_html_rows += f"""
                          <tr>
                            <td style=\"padding:6px 8px;color:#455a64;font-size:13px;border-bottom:1px solid #eceff1;\">{nombre}</td>
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
                      <td background="{FOOTER_GAS_IMAGE_URL}" style="background-image:url('{FOOTER_GAS_IMAGE_URL}');background-size:cover;background-position:center;padding:0;">
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:rgba(0,0,0,0.45);">
                          <tr>
                            <td style="padding:18px 24px;text-align:center;color:#ffffff;font-size:11px;line-height:1.5;">
                              Este es un mensaje automático relacionado con nuevas cotizaciones.
                            </td>
                          </tr>
                        </table>
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
        "Mensaje de contacto desde gamatec.org:\n\n"
        f"Nombre: {nombre}\n"
        f"Correo: {email}\n\n"
        f"Mensaje:\n{mensaje}"
    )

    html = f"""
        <html>
          <body style="margin:0;padding:0;background-color:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8;padding:20px 0;">
              <tr>
                <td align="center">
                  <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                    <tr>
                      <td style="background:linear-gradient(90deg,#0d47a1,#1976d2);padding:20px 24px;color:#ffffff;">
                        <h1 style="margin:0;font-size:22px;font-weight:600;">Nuevo mensaje de contacto</h1>
                        <p style="margin:4px 0 0;font-size:14px;opacity:0.9;">Has recibido un nuevo mensaje desde la landing.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:24px;background-color:#ffffff;">
                        <p style="margin:0 0 16px;color:#37474f;font-size:14px;">Hola,</p>
                        <p style="margin:0 0 16px;color:#455a64;font-size:14px;">
                          Estos son los datos del contacto recibido:
                        </p>
                        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:14px;">
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;width:150px;">Nombre:</td>
                            <td style="padding:8px 0;color:#263238;font-weight:600;">{nombre}</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;color:#607d8b;">Correo:</td>
                            <td style="padding:8px 0;color:#1976d2;font-weight:600;">{email}</td>
                          </tr>
                        </table>
                        <p style="margin:24px 0 8px;color:#37474f;font-size:14px;font-weight:600;">Mensaje</p>
                        <div style="padding:12px 14px;background-color:#fafbfc;border-radius:6px;border:1px solid #eceff1;color:#455a64;font-size:14px;line-height:1.5;">
                          {mensaje.replace('\n', '<br>')}
                        </div>
                        <p style="margin:24px 0 0;color:#78909c;font-size:12px;">
                          Te recomendamos dar seguimiento a este mensaje a la brevedad.
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td background="{FOOTER_GAS_IMAGE_URL}" style="background-image:url('{FOOTER_GAS_IMAGE_URL}');background-size:cover;background-position:center;padding:0;">
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:rgba(0,0,0,0.45);">
                          <tr>
                            <td style="padding:18px 24px;text-align:center;color:#ffffff;font-size:11px;line-height:1.5;">
                              Este es un mensaje automático generado desde el formulario de contacto de la landing.
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
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
