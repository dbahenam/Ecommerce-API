from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer

@extend_schema(responses=CategorySerializer)
class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Categories
    """
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        print(serializer.data) # list of dictionaries
        return Response(serializer.data) # Http response object with data as json
    
@extend_schema(responses=BrandSerializer)
class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Brands
    """
    queryset = Brand.objects.all()

    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)

@extend_schema(responses=ProductSerializer)
class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Products
    """
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)



