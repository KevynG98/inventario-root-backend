from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.inventarioPrecioSkuModel import PrecioSKU
from ..serializers.inventarioPrecioSkuSerializer import PrecioSKUSerializer

@api_view(['GET'])
def listar_precios(request):
    precios = PrecioSKU.objects.filter(is_active=True)
    serializer = PrecioSKUSerializer(precios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_precio(request):
    print(request.data)
    serializer = PrecioSKUSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_precio(request, pk):
    try:
        precio = PrecioSKU.objects.get(pk=pk, is_active=True)
    except PrecioSKU.DoesNotExist:
        return Response({"error": "Precio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    print("🔍 Datos recibidos:", request.data)  # 👈 Agrega esto para debug

    serializer = PrecioSKUSerializer(precio, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("❌ Errores del serializer:", serializer.errors)  # 👈 Esto también ayuda
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_precio(request, pk):
    try:
        precio = PrecioSKU.objects.get(pk=pk, is_active=True)
        precio.is_active = False
        precio.save()
        return Response({"message": "Precio eliminado (soft delete)"}, status=status.HTTP_200_OK)
    except PrecioSKU.DoesNotExist:
        return Response({"error": "Precio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
