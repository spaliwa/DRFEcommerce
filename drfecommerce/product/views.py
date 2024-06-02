from django.shortcuts import render
from django.db import connection
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, ProductLineSerializer

# Create your views here.

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """
    queryset = Category.objects.all()
    
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

class BrandViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for viewing all brands
    """

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    

class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for Viewing all products
    """
    queryset = Product.objects.all().isactive()

    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.Product.filter(slug=slug).select_related("category", "brand").prefetch_related(Prefetch("product_line_product_image")),
            many=True,
        )
        data = Response(serializer.data)
        return data
    
    @extend_schema(responses=ProductLineSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(
        methods=["get"],
        detail= False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category_slug=slug), many=True
        )
        return Response(serializer.data)