from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from collections import defaultdict
from rest_framework.generics import get_object_or_404

from api.utils.pagination import CustomPageNumberPagination
from ..models.admisionesModel import Admision
from ..serializers.admisionesSerializer import (
    AdmisionCreateSerializer,
    AdmisionUpdateFlatSerializer,
    AdmisionDetalleSerializer,
    EstadoCuentaSerializer,
    MovimientoCuentaSerializer
)
from api.models import Habitacion
from api.models import Seguros

# 🔹 Crear admisión (POST - datos planos)
@api_view(['POST'])
def crear_admision(request):
    serializer = AdmisionCreateSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        admision = serializer.save()
        return Response({"message": "Admisión creada correctamente", "id": admision.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_admision(request, admision_id):
    try:
        admision = Admision.objects.get(pk=admision_id)
    except Admision.DoesNotExist:
        return Response({"error": "Admisión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdmisionDetalleSerializer(admision)
    data = serializer.data

    # 🔍 Buscar info de la habitación por ID plana (si no hay relación habitacion_fk)
    habitacion_data = None
    if admision.habitacion and not admision.habitacion_fk:
        try:
            habitacion_obj = Habitacion.objects.get(id=int(admision.habitacion))
            habitacion_data = {
                "id": habitacion_obj.id,
                "codigo": habitacion_obj.codigo,
                "area": habitacion_obj.area,
                "estado": habitacion_obj.estado,
                "nivel": habitacion_obj.nivel,
                "paciente": habitacion_obj.paciente,
                "observacion": habitacion_obj.observacion,
            }
        except (Habitacion.DoesNotExist, ValueError):
            habitacion_data = None

    # 🔁 Inyectar la habitación si habitacion_fk está vacía
    if habitacion_data:
        data["habitacion_fk"] = habitacion_data

    return Response(data, status=status.HTTP_200_OK)

# 🔹 Listar agrupadas por área (GET - sin paginación)
@api_view(['GET'])
def listar_admisiones_por_area(request):
    admisiones = Admision.objects.select_related('paciente').all()
    agrupadas = defaultdict(list)
    for admision in admisiones:
        serialized = AdmisionDetalleSerializer(admision).data
        area = admision.area_admision or "Sin área"
        agrupadas[area].append(serialized)
    return Response(agrupadas, status=status.HTTP_200_OK)

# 🔹 Resumen por área (GET - sin paginación)
@api_view(['GET'])
def resumen_admisiones_por_area(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').all()
    agrupadas = defaultdict(list)
    for admision in admisiones:
        paciente = admision.paciente
        area = admision.area_admision or "Sin área"
        resumen = {
            "id_admision": admision.id,
            "fecha_admision": admision.fecha.strftime('%Y-%m-%d'),
            "paciente": paciente.nombre,
            "identificacion": paciente.numero_identificacion,
            "genero": getattr(paciente, "genero", "N/A"),
            "aseguradora": admision.datos_seguro.aseguradora if admision.datos_seguro else "N/A",
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico_tratante": admision.medico_tratante
        }
        agrupadas[area].append(resumen)
    return Response(agrupadas, status=status.HTTP_200_OK)

@api_view(['GET'])
def listar_admisiones_resumen(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').order_by('id')
    paginator = CustomPageNumberPagination()
    resultado = paginator.paginate_queryset(admisiones, request)

    data = []
    for admision in resultado:
        paciente = admision.paciente

        nombre_completo = " ".join(filter(None, [
            paciente.primer_nombre,
            paciente.segundo_nombre,
            paciente.primer_apellido,
            paciente.segundo_apellido,
            paciente.apellido_casada
        ]))

        fecha_nac = paciente.fecha_nacimiento.strftime('%d/%m/%Y') if paciente.fecha_nacimiento else "N/D"
        fecha_adm = admision.fecha.strftime('%d/%m/%Y') if admision.fecha else "N/D"

        # 🔍 Buscar nombre aseguradora manualmente
        aseguradora_nombre = "SIN SEGURO"
        if admision.datos_seguro and admision.datos_seguro.aseguradora:
            try:
                aseguradora_obj = Seguros.objects.get(id=int(admision.datos_seguro.aseguradora))
                aseguradora_nombre = aseguradora_obj.nombre
            except (Seguros.DoesNotExist, ValueError):
                aseguradora_nombre = f"ID {admision.datos_seguro.aseguradora}"

        # 🔍 Resolver habitación usando la FK cuando exista
        habitacion_obj = admision.habitacion_fk
        if not habitacion_obj and admision.habitacion:
            try:
                habitacion_obj = Habitacion.objects.get(id=int(admision.habitacion))
            except (Habitacion.DoesNotExist, ValueError):
                habitacion_obj = None

        habitacion_str = (
            f"{habitacion_obj.codigo}"
            if habitacion_obj else "SIN CAMA"
        )

        data.append({
            "id_admision": admision.id,
            "fecha_admision": fecha_adm,
            "paciente": f"{nombre_completo} (NAC: {fecha_nac})",
            "identificacion": f"{paciente.tipo_identificacion or 'N/A'}: {paciente.numero_identificacion or 'N/A'}",
            "genero": paciente.genero or "N/D",
            "tipo_sangre": paciente.tipo_sangre or "N/D",
            "aseguradora": aseguradora_nombre,
            "area": admision.area_admision or "N/D",
            "habitacion": habitacion_str,
            "medico_tratante": admision.medico_tratante or "N/D"
        })

    return paginator.get_paginated_response(data)


# 🔹 Editar admisión (PUT - datos anidados) 
@api_view(['PUT'])
def editar_admision(request, pk):
    try:
        admision = Admision.objects.get(pk=pk)
    except Admision.DoesNotExist:
        return Response({'error': 'Admisión no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdmisionUpdateFlatSerializer(admision, data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Admisión actualizada correctamente"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listar_admisiones_estado(request):
    admisiones = Admision.objects.select_related('paciente', 'datos_seguro').order_by('-fecha')

    data = []
    for admision in admisiones:
        paciente = admision.paciente
        datos_seguro = admision.datos_seguro

        data.append({
            "id_admision": admision.id,
            "fecha_admision": admision.fecha.strftime('%d/%m/%Y') if admision.fecha else '',
            "paciente": " ".join(f"{paciente.primer_nombre} {paciente.segundo_nombre or ''} {paciente.primer_apellido} {paciente.segundo_apellido or ''} {paciente.apellido_casada or ''}".split()),
            "identificacion": f"{paciente.tipo_identificacion}: {paciente.numero_identificacion}",
            "genero": paciente.genero,
            "aseguradora": datos_seguro.aseguradora if datos_seguro else '',
            "area": admision.area_admision,
            "habitacion": admision.habitacion,
            "medico": admision.medico_tratante,
            "estado": admision.estado,
        })

    return Response(data)

@api_view(['GET'])
def estado_cuenta(request, admision_id):
    admision = get_object_or_404(Admision, pk=admision_id)
    serializer = EstadoCuentaSerializer(admision)
    return Response(serializer.data)

@api_view(['POST'])
def crear_movimiento(request):
    serializer = MovimientoCuentaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def generar_estado_cuenta_pdf(request, admision_id):
    admision = get_object_or_404(Admision, pk=admision_id)
    serializer = EstadoCuentaSerializer(admision)
    data = serializer.data

    agrupado = defaultdict(list)
    for mov in data.get("movimientos", []):
        categoria = mov.get("categoria", "Sin categoría")
        agrupado[categoria].append(mov)

    agrupado_lista = list(agrupado.items())

    # ✅ Ruta absoluta al logo
    logo_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'img', 'el-naranjo.png')

    html_string = render_to_string('estado_cuenta.html', {
        'data': data,
        'movimientos_por_categoria': agrupado_lista,
        'logo_path': f'file://{logo_path}',
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="estado_cuenta_{admision_id}.pdf"'
    return response

# 🔹 ListView (no modificada)
class ListadoAdmisionesView(ListAPIView):
    queryset = Admision.objects.all()
    serializer_class = AdmisionDetalleSerializer
