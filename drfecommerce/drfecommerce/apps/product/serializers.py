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
        exclude = ["product", "order"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = models.AttributeValue
        fields = ["attribute", "value"]


class ProductSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    product_line = serializers.CharField(source="product_line.name")
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = models.Product
        fields = [
            "product_line",
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        ]

    def to_representation(self, instance):
        represenation = super().to_representation(instance)
        attribute_values_data = represenation.pop("attribute_value")
        attribute_values = {}
        for key in attribute_values_data:
            attribute_values.update({key["attribute"]["id"]: key["value"]})
        represenation.update({"specifications": attribute_values})
        return represenation


class ProductLineSerializer(serializers.ModelSerializer):
    # The source argument in a serializer field tells the serializer where
    # to pull the data from when it's serializing a model instance or where
    # to push the data to when it's deserializing a payload into a model instance.

    # specific field names to not have to output whole brand/category serializer object
    brand_name = serializers.CharField(source="brand.name")
    category_slug = serializers.CharField(source="category.slug")
    product = ProductSerializer(many=True)  # has to match related_name
    # lines_of_product = ProductLineSerializer(source='product_line', many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductLine
        fields = [
            "name",
            "slug",
            "description",
            "brand_name",
            "category_slug",
            "product",
            "attribute",
        ]

    def get_attribute(self, obj):
        attribute = models.Attribute.objects.filter(
            product_type__product_line__id=obj.id
        )
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        represenation = super().to_representation(instance)
        attribute_data = represenation.pop("attribute")
        attribute_values = {}
        for key in attribute_data:
            attribute_values.update({key["id"]: key["name"]})
        represenation.update({"Type Specifications": attribute_values})
        return represenation
