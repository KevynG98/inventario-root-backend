from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.utils.pagination import CustomPageNumberPagination
from ..models.inventariosSkuModel import InventarioSKU, BodegaSKU
from ..serializers.inventarioSkuSerializer import InventarioSKUSerializer, MovimientoBodegaSerializer

@api_view(['GET'])
def listar_skus(request):
    skus = InventarioSKU.objects.filter(is_active=True).all().order_by('-id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(skus, request)
    serializer = InventarioSKUSerializer(result_page, many=True)
    return Response({
        "count": paginator.page.paginator.count,
        "total_pages": paginator.page.paginator.num_pages,
        "current_page": paginator.page.number,
        "page_size": paginator.get_page_size(request),
        "from": paginator.page.start_index(),
        "to": paginator.page.end_index(),
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": serializer.data
    })

@api_view(['POST'])
def crear_sku(request):
    serializer = InventarioSKUSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_sku(request, pk):
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioSKUSerializer(sku)
    return Response(serializer.data)

@api_view(['PUT'])
def actualizar_sku(request, pk):
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = InventarioSKUSerializer(sku, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_sku(request, pk):
    print(f"Eliminando SKU con ID: {pk}")
    try:
        sku = InventarioSKU.objects.get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({"error": "SKU no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    sku.is_active = False
    sku.save()
    return Response({"mensaje": "SKU desactivado (soft delete)"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def mover_producto(request):
    serializer = MovimientoBodegaSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        sku = data['sku']
        origen = data['bodega_origen']
        destino = data['bodega_destino']
        cantidad = data['cantidad']

        # Verificar existencia en bodega origen
        try:
            stock_origen = BodegaSKU.objects.get(sku=sku, nombre_bodega=origen)
        except BodegaSKU.DoesNotExist:
            return Response({"error": "La bodega de origen no tiene stock del producto"}, status=400)

        if stock_origen.cantidad < cantidad:
            return Response({"error": "No hay suficiente stock en la bodega de origen"}, status=400)

        # Descontar del origen
        stock_origen.cantidad -= cantidad
        stock_origen.save()

        # Agregar al destino
        stock_destino, created = BodegaSKU.objects.get_or_create(sku=sku, nombre_bodega=destino, defaults={'cantidad': 0})
        stock_destino.cantidad += cantidad
        stock_destino.save()

        # Guardar el movimiento
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def listar_skus_con_bodegas(request):
    queryset = InventarioSKU.objects.prefetch_related('bodegas').all().order_by('nombre')

    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = InventarioSKUSerializer(result_page, many=True)

    return Response({
        "count": paginator.page.paginator.count,
        "total_pages": paginator.page.paginator.num_pages,
        "current_page": paginator.page.number,
        "page_size": paginator.get_page_size(request),
        "from": paginator.page.start_index(),
        "to": paginator.page.end_index(),
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": serializer.data
    })
    
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def detalle_sku_con_bodegas(request, pk):
    try:
        sku = InventarioSKU.objects.prefetch_related('bodegas').get(pk=pk)
    except InventarioSKU.DoesNotExist:
        return Response({'error': 'SKU no encontrado'}, status=404)

    serializer = InventarioSKUSerializer(sku)
    return Response(serializer.data)
