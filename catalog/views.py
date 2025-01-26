from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Category, Product
from catalog.serializers import (CategorySerializer,
                                 ProductSerializer)


class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'free_delivery', 'available']
    ordering_fields = ['price', 'rating', 'reviews', 'created_at']
    ordering = ['created_at']
    pagination_class = None
