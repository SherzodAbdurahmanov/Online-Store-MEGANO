from rest_framework import status, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog import models
from catalog.models import (Category,
                            Product,
                            SaleItem,
                            Banner,
                            BasketItem,
                            Tag, Review)
from catalog.serializers import (CategorySerializer,
                                 ProductSerializer,
                                 SaleItemSerializer,
                                 BannerSerializer,
                                 BasketItemSerializer,
                                 TagSerializer, ReviewSerializer)


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


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularProductsView(APIView):
    def get(self, request):
        products = Product.objects.order_by('-rating', '-reviews')[:10]  # Топ-10 популярных
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Достаем данные из запроса
        text = request.data.get("text")
        rating = request.data.get("rating")

        # Проверяем корректность рейтинга
        if not (1 <= int(rating) <= 5):
            return Response({"error": "Рейтинг должен быть от 1 до 5"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем отзыв
        review = Review.objects.create(user=request.user, product=product, text=text, rating=rating)

        # Пересчитываем средний рейтинг продукта
        avg_rating = Review.objects.filter(product=product).aggregate(models.Avg('rating'))['rating__avg']
        product.rating = round(avg_rating, 1)
        product.reviews = Review.objects.filter(product=product).count()
        product.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class BasketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Получить все товары в корзине текущего пользователя
        basket_items = BasketItem.objects.filter(user=request.user)
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Добавить товар в корзину
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Найти или создать элемент корзины
        basket_item, created = BasketItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            basket_item.quantity += int(quantity)  # Увеличиваем количество
        else:
            basket_item.quantity = int(quantity)
        basket_item.save()

        serializer = BasketItemSerializer(basket_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        # Удалить товар из корзины
        product_id = request.data.get("product_id")

        try:
            basket_item = BasketItem.objects.get(user=request.user, product_id=product_id)
            basket_item.delete()
            return Response({"message": "Товар удален из корзины"}, status=status.HTTP_200_OK)
        except BasketItem.DoesNotExist:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)


class TagsView(APIView):
    def get(self, request):
        category_id = request.query_params.get("category")

        if category_id:
            tags = Tag.objects.filter(category_id=category_id)
        else:
            tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
