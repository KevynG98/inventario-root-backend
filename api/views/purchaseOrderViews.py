from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.purchaseOrderModel import PurchaseOrder
from ..serializers.purchaseOrderSerializer import PurchaseOrderSerializer

@api_view(['GET'])
def list_purchase_orders(request):
    orders = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_purchase_order(request, order_id):
    try:
        order = PurchaseOrder.objects.get(id=order_id)
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=404)

@api_view(['PUT'])
def update_purchase_order(request, order_id):
    try:
        order = PurchaseOrder.objects.get(id=order_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=404)

    serializer = PurchaseOrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_purchase_order(request, order_id):
    try:
        order = PurchaseOrder.objects.get(id=order_id)
        order.delete()
        return Response({"message": "Purchase order deleted"}, status=204)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=404)
