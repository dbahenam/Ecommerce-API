from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Categories
    """
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        print(serializer.data) # list of dictionaries
        return Response(serializer.data) # Http response object with data as json
    

class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Brands
    """
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Products
    """
    queryset = Product.objects.all()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(self.queryset.filter(slug=slug), many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

    @action(
        methods=["get"], 
        detail=False, 
        url_path=r"category/(?P<cat_name>\w+)/all",
        url_name="all"
    )
    def list_product_by_category(self, request, cat_name=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__name=cat_name), many=True)
        return Response(serializer.data)



