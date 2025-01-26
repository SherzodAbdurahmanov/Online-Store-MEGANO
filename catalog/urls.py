from django.urls import path

from catalog.views import CategoriesView, ProductListView

app_name = 'catalog'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
]
