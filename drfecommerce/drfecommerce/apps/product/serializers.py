from rest_framework import serializers
from .models import Category, Brand, Product, ProductLine

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    # Connecion to other serializers
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["name", "description", "is_digital", "is_active", "brand", "category"]

class ProductLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductLine
        fields = "__all__"