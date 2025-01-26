from django.db import models


class Category(models.Model):
    """Модель для хранения категории"""
    title = models.CharField(max_length=255, null=True)
    image_src = models.URLField(max_length=200, null=True)  # URL для изображения
    image_alt = models.CharField(max_length=255, null=True)  # Альтернативный текст для изображения

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель для хранения продуктов"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    free_delivery = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
