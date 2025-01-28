from rest_framework import serializers
from catalog.models import (Category,
                            Product,
                            SaleItem,
                            Banner)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image_src', 'image_alt']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'description', 'price', 'count',
            'free_delivery', 'available', 'stock', 'rating', 'reviews', 'created_at'
        ]


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'sale_price', 'date_from', 'date_to']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'url']
