from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from django.db import connection, reset_queries
from drfecommerce.apps.utils.sql_debugger import SqlDebugger

from .models import Brand, Category, Product, ProductLine
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductLineSerializer,
)


# Let drf_spectacular know which schema we are using
@extend_schema(responses=CategorySerializer)
class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Categories
    """

    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        print(serializer.data)  # list of dictionaries
        return Response(serializer.data)  # Http response object with data as json


@extend_schema(responses=BrandSerializer)
class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Brands
    """

    queryset = Brand.objects.is_active()

    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


@extend_schema(responses=ProductSerializer)
class ProductLineViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing Products
    """

    queryset = ProductLine.objects.is_active()
    lookup_field = "slug"  # default is pk

    def retrieve(self, request, slug=None):
        reset_queries()
        serializer = ProductLineSerializer(
            self.queryset.filter(slug=slug)
            .select_related("category", "brand")  # INNER JOINS
            .prefetch_related(  # 1-N, N-N, Reverse Foreign Keys
                "product__product_image"
            ),
            many=True,
        )

        data = Response(serializer.data)

        debugger = SqlDebugger()
        for query in connection.queries:
            debugger.set_data(query["sql"])
            debugger.print_sql()

        return data

    def list(self, request):
        serializer = ProductLineSerializer(self.queryset, many=True)
        return Response(serializer.data)

    #
    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<cat_slug>[\w-]+)/all",  # regex
        url_name="all",
    )
    def list_product_line_by_category_slug(self, request, cat_slug=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductLineSerializer(
            self.queryset.filter(category__slug=cat_slug), many=True
        )
        return Response(serializer.data)


@extend_schema(responses=ProductLineSerializer)
class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        # print(serializer.data)
        return Response(serializer.data)
