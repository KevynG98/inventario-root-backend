from rest_framework import serializers
from ..models.inventoryMovementsModel import InventoryMovement

class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = '__all__'
