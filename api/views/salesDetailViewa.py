from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.salesDetailModel import SaleDetail
from ..serializers.salesDetailSerializer import SaleDetailSerializer

@api_view(['GET'])
def list_sale_details(request):
    details = SaleDetail.objects.all()
    serializer = SaleDetailSerializer(details, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_sale_detail(request):
    serializer = SaleDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_sale_detail(request, pk):
    try:
        detail = SaleDetail.objects.get(pk=pk)
        serializer = SaleDetailSerializer(detail)
        return Response(serializer.data)
    except SaleDetail.DoesNotExist:
        return Response({"error": "Sale detail not found"}, status=404)

@api_view(['PUT'])
def update_sale_detail(request, pk):
    try:
        detail = SaleDetail.objects.get(pk=pk)
    except SaleDetail.DoesNotExist:
        return Response({"error": "Sale detail not found"}, status=404)

    serializer = SaleDetailSerializer(detail, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_sale_detail(request, pk):
    try:
        detail = SaleDetail.objects.get(pk=pk)
        detail.delete()
        return Response({"message": "Sale detail deleted"}, status=204)
    except SaleDetail.DoesNotExist:
        return Response({"error": "Sale detail not found"}, status=404)
