from rest_framework import serializers
from ..models.salesDetailModel import SaleDetail

class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__'
