from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models.inventoryModel import Inventory
from ..serializers.inventorySerializer import InventorySerializer

@api_view(['GET'])
def list_inventory(request):
    inventory = Inventory.objects.all()
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_inventory(request):
    serializer = InventorySerializer(data=request.data)
    
    if serializer.is_valid():
        product = serializer.validated_data['product']
        requested_quantity = serializer.validated_data['quantity']

        # Verificar si hay suficiente stock
        if product.quantity < requested_quantity:
            return Response(
                {"message": "Error: Not enough stock available for this product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el registro de inventario
        inventory = serializer.save()

        # Actualizar cantidad en la tabla Product
        product.quantity -= requested_quantity
        product.save()

        # Verificar si el producto se quedó sin stock
        message = "Inventory created successfully"
        if product.quantity <= 0:
            message += " - Warning: This product is out of stock!"

        return Response({"message": message, "data": serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    serializer = InventorySerializer(inventory)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    previous_quantity = inventory.quantity  # Guardar la cantidad anterior

    serializer = InventorySerializer(inventory, data=request.data, partial=True)
    if serializer.is_valid():
        updated_inventory = serializer.save()

        # Ajustar la cantidad en Product
        difference = updated_inventory.quantity - previous_quantity
        updated_inventory.product.quantity += difference
        updated_inventory.product.save()

        # Verificar si el producto quedó sin stock
        message = "Inventory updated successfully"
        if updated_inventory.product.quantity <= 0:
            message += " - Warning: This product is out of stock!"

        return Response({"message": message, "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def mark_inventory_as_used(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    # Marcar como usado
    inventory.status = 'used'
    inventory.save()

    return Response({"message": "Inventory marked as used"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def available_inventory(request):
    status_filter = request.query_params.get('status')  # Obtiene el estado desde la URL

    if status_filter in ['available', 'used']:  
        inventory = Inventory.objects.filter(status=status_filter)
    else:
        inventory = Inventory.objects.all()  # Si no hay filtro, devuelve todo

    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)
