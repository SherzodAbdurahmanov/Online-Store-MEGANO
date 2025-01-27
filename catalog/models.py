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
    stock = models.PositiveIntegerField()
    rating = models.FloatField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SaleItem(models.Model):
    """Модель для хранения товаров на распродаже"""
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name="sale")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return f"Sale for {self.product.title}"


class Banner(models.Model):
    """Модель для хранения баннеров"""
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/")
    url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title
