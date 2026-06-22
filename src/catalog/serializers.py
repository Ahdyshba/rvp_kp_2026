from rest_framework import serializers
from .models import Product, Category, CategoryAttribute

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')
    attribute_type = serializers.CharField(source='attribute.attribute_type')
    
    class Meta:
        model = CategoryAttribute
        fields = ['id', 'category', 'attribute', 'attribute_name', 'attribute_type', 'is_required', 'is_filter']