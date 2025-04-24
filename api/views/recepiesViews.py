from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.recepiesModels import Receta, RecetaDetalle, Medicamento
from ..serializers.recepiesSerializer import RecetaSerializer

# Crear una receta (Solo Doctor o Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_receta(request):
    usuario = request.user

    # Solo doctores y administradores pueden crear recetas
    if not (usuario.groups.filter(name="doctor").exists() or usuario.is_superuser):
        return Response({"error": "Solo doctores o administradores pueden crear recetas."}, status=403)

    data = request.data
    paciente_id = data.get("paciente_id")
    medicamentos = data.get("medicamentos", [])

    receta = Receta.objects.create(paciente_id=paciente_id, doctor=usuario)

    for med in medicamentos:
        RecetaDetalle.objects.create(
            receta=receta,
            medicamento_id=med["medicamento_id"],
            cantidad=med["cantidad"]
        )

    return Response({"message": f"Receta {receta.id} creada correctamente"}, status=201)

# Procesar receta en caja (Solo Enfermera o Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def procesar_receta(request, receta_id):
    usuario = request.user

    # Solo enfermeras y administradores pueden procesar recetas
    if not (usuario.groups.filter(name="enfermera").exists() or usuario.is_superuser):
        return Response({"error": "Solo enfermeras o administradores pueden procesar recetas."}, status=403)

    receta = get_object_or_404(Receta, id=receta_id, procesada=False)

    # Verificar stock
    for detalle in receta.detalles.all():
        if detalle.medicamento.stock < detalle.cantidad:
            return Response({"error": f"No hay suficiente stock de {detalle.medicamento.nombre}"}, status=400)

    # Descontar stock
    for detalle in receta.detalles.all():
        detalle.medicamento.stock -= detalle.cantidad
        detalle.medicamento.save()

    receta.procesada = True
    receta.save()

    return Response({"message": f"Receta {receta.id} procesada correctamente"}, status=200)

# Listar todas las recetas (Para cualquier usuario autenticado)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_recetas(request):
    recetas = Receta.objects.all()
    serializer = RecetaSerializer(recetas, many=True)
    return Response(serializer.data)

# Obtener una receta por ID (Para cualquier usuario autenticado)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    serializer = RecetaSerializer(receta)
    return Response(serializer.data)

# Eliminar una receta (Solo Doctor o Administrador)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_receta(request, receta_id):
    usuario = request.user

    # Solo doctores y administradores pueden eliminar recetas
    if not (usuario.groups.filter(name="doctor").exists() or usuario.is_superuser):
        return Response({"error": "Solo doctores o administradores pueden eliminar recetas."}, status=403)

    receta = get_object_or_404(Receta, id=receta_id)
    receta.delete()
    return Response({"message": f"Receta {receta_id} eliminada correctamente"}, status=200)