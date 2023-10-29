from rest_framework import serializers
from .models import Category, Brand, Product, ProductLine

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]

class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ["id", "is_active", "product"]

class ProductSerializer(serializers.ModelSerializer):
    """
    The source argument in a serializer field tells the serializer where 
    to pull the data from when it's serializing a model instance or where
    to push the data to when it's deserializing a payload into a model instance.
    """
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True) # same as the line below
    # lines_of_product = ProductLineSerializer(source='product_line', many=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "description", "brand_name", "category_name", "product_line"]