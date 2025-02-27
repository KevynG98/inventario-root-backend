from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.purchaseOrderDetailModel import PurchaseOrderDetail
from ..serializers.purchaseOrderDetailSerializer import PurchaseOrderDetailSerializer

@api_view(['GET'])
def list_purchase_order_details(request):
    details = PurchaseOrderDetail.objects.all()
    serializer = PurchaseOrderDetailSerializer(details, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_purchase_order_detail(request):
    serializer = PurchaseOrderDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_purchase_order_detail(request, pk):
    try:
        detail = PurchaseOrderDetail.objects.get(pk=pk)
        serializer = PurchaseOrderDetailSerializer(detail)
        return Response(serializer.data)
    except PurchaseOrderDetail.DoesNotExist:
        return Response({"error": "Purchase order detail not found"}, status=404)

@api_view(['PUT'])
def update_purchase_order_detail(request, pk):
    try:
        detail = PurchaseOrderDetail.objects.get(pk=pk)
    except PurchaseOrderDetail.DoesNotExist:
        return Response({"error": "Purchase order detail not found"}, status=404)

    serializer = PurchaseOrderDetailSerializer(detail, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_purchase_order_detail(request, pk):
    try:
        detail = PurchaseOrderDetail.objects.get(pk=pk)
        detail.delete()
        return Response({"message": "Purchase order detail deleted"}, status=204)
    except PurchaseOrderDetail.DoesNotExist:
        return Response({"error": "Purchase order detail not found"}, status=404)
