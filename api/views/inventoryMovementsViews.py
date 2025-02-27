from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.inventoryMovementsModel import InventoryMovement
from ..serializers.inventoryMovementsSerializer import InventoryMovementSerializer

@api_view(['GET'])
def list_inventory_movements(request):
    movements = InventoryMovement.objects.all()
    serializer = InventoryMovementSerializer(movements, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_inventory_movement(request):
    serializer = InventoryMovementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_inventory_movement(request, movement_id):
    try:
        movement = InventoryMovement.objects.get(id=movement_id)
        serializer = InventoryMovementSerializer(movement)
        return Response(serializer.data)
    except InventoryMovement.DoesNotExist:
        return Response({"error": "Inventory movement not found"}, status=404)

@api_view(['PUT'])
def update_inventory_movement(request, movement_id):
    try:
        movement = InventoryMovement.objects.get(id=movement_id)
    except InventoryMovement.DoesNotExist:
        return Response({"error": "Inventory movement not found"}, status=404)

    serializer = InventoryMovementSerializer(movement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_inventory_movement(request, movement_id):
    try:
        movement = InventoryMovement.objects.get(id=movement_id)
        movement.delete()
        return Response({"message": "Inventory movement deleted"}, status=204)
    except InventoryMovement.DoesNotExist:
        return Response({"error": "Inventory movement not found"}, status=404)
