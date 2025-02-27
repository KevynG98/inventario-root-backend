from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.salesModel import Sale
from ..serializers.salesSerializar import SaleSerializer

@api_view(['GET'])
def list_sales(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_sale(request):
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=404)

@api_view(['PUT'])
def update_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=404)

    serializer = SaleSerializer(sale, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
        sale.delete()
        return Response({"message": "Sale deleted"}, status=204)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=404)
