from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing categories
    """
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        print(serializer.data) # list of dictionaries
        return Response(serializer.data) # Http response object with data as json

