from rest_framework import serializers
from ..models.purchaseOrderDetailModel import PurchaseOrderDetail

class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderDetail
        fields = '__all__'
