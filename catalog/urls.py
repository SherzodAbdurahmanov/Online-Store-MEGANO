from django.urls import path

from catalog.views import (CategoriesView,
                           ProductListView,
                           PopularProductsView,
                           LimitedProductsView,
                           SalesView,
                           BannersView,
                           BasketView,
                           TagsView,
                           ProductDetailView,
                           ProductReviewView)

app_name = 'catalog'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('products/popular/', PopularProductsView.as_view(), name='products_popular'),
    path('products/limited/', LimitedProductsView.as_view(), name='products_limited'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/review/', ProductReviewView.as_view(), name='product_review'),
    path('sales/', SalesView.as_view(), name='sales'),
    path('banners/', BannersView.as_view(), name='banners'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('tags/', TagsView.as_view(), name='tags'),
]
