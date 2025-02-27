from rest_framework import serializers
from ..models.productModel import Product
from .categorySerializer import CategorySerializer
from ..models.categoryModel import Category

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_id', 'price', 'unit', 'created_at', 'updated_at']
