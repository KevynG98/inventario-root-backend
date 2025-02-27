from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.productModel import Product
from ..serializers.productSerializer import ProductSerializer

@api_view(['GET'])
def list_products(request):
    products = Product.objects.filter(is_deleted=False)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
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
    product = Product.objects.filter(id=pk, is_deleted=False).first()
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
    
    product.is_deleted = True
    product.save()
    return Response({"message": "Product marked as deleted"}, status=200)
