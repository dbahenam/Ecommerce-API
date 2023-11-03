from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ["name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        exclude = ["productline", "id"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = models.ProductLine
        fields = ["price", "sku", "stock_qty", "order", "product_image"]


class ProductSerializer(serializers.ModelSerializer):
    # The source argument in a serializer field tells the serializer where
    # to pull the data from when it's serializing a model instance or where
    # to push the data to when it's deserializing a payload into a model instance.
    brand_name = serializers.CharField(source="brand.name")
    category_slug = serializers.CharField(source="category.slug")
    product_line = ProductLineSerializer(many=True)  # same as the line below
    # lines_of_product = ProductLineSerializer(source='product_line', many=True)

    class Meta:
        model = models.Product
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_slug",
            "product_line",
        ]
