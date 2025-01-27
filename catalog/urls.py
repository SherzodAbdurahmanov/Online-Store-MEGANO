from django.urls import path

from catalog.views import (CategoriesView,
                           ProductListView,
                           PopularProductsView,
                           LimitedProductsView,
                           SalesView,
                           BannersView)

app_name = 'catalog'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('products/popular/', PopularProductsView.as_view(), name='products_popular'),
    path('products/limited/', LimitedProductsView.as_view(), name='products_limited'),
    path('sales/', SalesView.as_view(), name='sales'),
    path('banners/', BannersView.as_view(), name='banners'),
]
