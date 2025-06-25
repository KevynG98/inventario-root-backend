from rest_framework.decorators import api_view, authentication_classes, permission_classes
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from django.http import HttpResponse

@api_view(['POST'])
def generar_receta_pdf(request):
    if request.method != 'POST':
        return HttpResponse("Método no permitido", status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))  # Convertir JSON a diccionario
    except json.JSONDecodeError:
        return HttpResponse("Error en el formato del JSON", status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="receta.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Datos del doctor
    doctor = data.get("doctor", {})
    paciente = data.get("paciente", "Paciente Desconocido")
    medicamentos = data.get("medicamentos", [])
    otras_indicaciones = data.get("otras_indicaciones", "")

    # Encabezado Doctor
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 50, doctor.get("nombre", "Dr. Nombre Apellido"))

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, height - 65, f"Céd. Prof. {doctor.get('cedula', '00000')}")
    c.drawString(50, height - 80, doctor.get("especialidad", ""))

    c.setFont("Helvetica", 9)
    c.drawString(50, height - 95, doctor.get("clinica", ""))
    c.drawString(50, height - 110, f"Teléfono: {doctor.get('telefono', '')}")
    c.drawString(50, height - 125, f"Correo electrónico: {doctor.get('correo', '')}")

    # Fecha y hora
    c.setFont("Helvetica", 9)
    fecha_hora = datetime.now().strftime("%d %b, %Y. %I:%M:%S %p")
    c.drawString(width - 150, height - 50, fecha_hora)

    # Línea divisoria
    c.line(50, height - 140, width - 50, height - 140)

    # Datos del paciente
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 160, f"Paciente: {paciente}")

    y_pos = height - 190  # Posición inicial

    # Medicamentos
    for med in medicamentos:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y_pos, med.get("nombre", "Medicamento Desconocido"))
        y_pos -= 15  # Espacio entre líneas

        c.setFont("Helvetica", 9)
        c.drawString(50, y_pos, med.get("dosis", ""))
        y_pos -= 25  # Espacio entre medicamentos

    # Otras indicaciones
    if otras_indicaciones:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y_pos, "Otras indicaciones")
        y_pos -= 15

        c.setFont("Helvetica", 9)
        c.drawString(50, y_pos, otras_indicaciones)
        y_pos -= 25

    # Línea para la firma
    c.line(100, 100, 250, 100)  # Línea de firma
    c.setFont("Helvetica", 9)
    c.drawString(100, 80, f"Firma {doctor.get('nombre', 'Dr. Nombre Apellido')}")

    c.save()
    return response
