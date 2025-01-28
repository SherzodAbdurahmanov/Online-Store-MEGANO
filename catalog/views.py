from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import (Category,
                            Product,
                            SaleItem,
                            Banner)
from catalog.serializers import (CategorySerializer,
                                 ProductSerializer,
                                 SaleItemSerializer,
                                 BannerSerializer)


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


class PopularProductsView(APIView):
    def get(self, request):
        products = Product.objects.order_by('-rating', '-reviews')[:10]  # Топ-10 популярных
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(stock__lt=10).order_by('stock')  # Продукты с ограниченным количеством
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesView(APIView):
    def get(self, request):
        sales = SaleItem.objects.all()
        serializer = SaleItemSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannersView(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
