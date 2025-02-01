from django.urls import path
from .views import (OrderView,
                    OrderDetailView,
                    PaymentView)

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order_detail'),
    path('payment/', PaymentView.as_view(), name='payment'),
]
