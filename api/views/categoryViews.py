from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.categoryModel import Category
from ..serializers.categorySerializer import CategorySerializer

@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_category(request, pk):
    category = Category.objects.filter(id=pk).first()
    if not category:
        return Response({"error": "Category not found"}, status=404)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['PUT'])
def update_category(request, pk):
    category = Category.objects.filter(id=pk).first()
    if not category:
        return Response({"error": "Category not found"}, status=404)
    
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_category(request, pk):
    category = Category.objects.filter(id=pk).first()
    if not category:
        return Response({"error": "Category not found"}, status=404)
    
    category.delete()
    return Response({"message": "Category deleted successfully"}, status=204)
