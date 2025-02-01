from rest_framework import serializers
from catalog.models import (Category,
                            Product,
                            SaleItem,
                            Banner,
                            BasketItem,
                            Tag, Review)


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


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'category']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'text', 'rating', 'created_at']
        read_only_fields = ['user', 'product', 'created_at']
