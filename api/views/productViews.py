from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.productModel import Product
from ..serializers.productSerializer import ProductSerializer
from ..utils.pagination import CustomPageNumberPagination
from django.db.models import Max

@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def create_product(request):
    print("Datos recibidos:", request.data)

    # Obtener el ID más alto existente y sumar 1
    max_id = Product.objects.aggregate(max_id=Max('id'))['max_id'] or 0
    next_id = max_id + 1

    # Hacer copia editable de request.data
    data = request.data.copy()
    data['id'] = next_id  # Establecer manualmente el ID

    serializer = ProductSerializer(data=data)
    
    if serializer.is_valid():
        instance = serializer.save()
        full_serializer = ProductSerializer(instance)
        return Response(full_serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_product(request, pk):
    product = Product.objects.filter(id=pk, is_deleted=False).first()
    if not product:
        return Response({"error": "Product not found"}, status=404)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['PUT'])
def update_product(request, pk):
    # product = Product.objects.filter(id=pk, is_deleted=False).first()
    product = Product.objects.filter(id=pk).first()
    if not product:
        return Response({"error": "Product not found"}, status=404)
    
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_product(request, pk):
    product = Product.objects.filter(id=pk).first()
    if not product:
        return Response({"error": "Product not found"}, status=404)
    
    # 🔥 Eliminar de forma definitiva por ahora:
    product.delete()

    # 💤 Si deseas usar soft delete más adelante, usa esto en su lugar:
    # product.is_deleted = True
    # product.save()

    return Response({"message": "Producto eliminado correctamente"}, status=204)
