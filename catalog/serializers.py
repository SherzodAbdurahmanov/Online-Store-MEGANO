from rest_framework import serializers
from catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image_src', 'image_alt']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'description', 'price', 'count',
            'free_delivery', 'available', 'rating', 'reviews', 'created_at'
        ]
