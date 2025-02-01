from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderItem, Payment
from .serializers import (OrderSerializer,
                          PaymentSerializer)


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Получить активный заказ пользователя
        order = Order.objects.filter(user=request.user, status='pending').first()
        if not order:
            return Response({"error": "Активный заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Создать новый заказ из корзины
        basket_items = request.user.basket_items.all()  # Предполагаем, что корзина связана с пользователем
        if not basket_items.exists():
            return Response({"error": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаём заказ
        order = Order.objects.create(user=request.user, total_cost=0)
        total_cost = 0

        # Добавляем товары из корзины
        for item in basket_items:
            total_cost += item.product.price * item.quantity
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity,
                                     price=item.product.price)

        # Обновляем итоговую стоимость
        order.total_cost = total_cost
        order.save()

        # Очищаем корзину
        basket_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        # Получить детали конкретного заказа
        try:
            order = Order.objects.get(id=id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        # Подтвердить заказ
        try:
            order = Order.objects.get(id=id, user=request.user, status='pending')
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден или уже подтвержден"}, status=status.HTTP_404_NOT_FOUND)

        order.status = 'confirmed'
        order.save()
        return Response({"message": "Заказ подтвержден"}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        method = request.data.get("method")

        # Проверяем, существует ли заказ
        try:
            order = Order.objects.get(id=order_id, user=request.user, status="confirmed")
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден или не подтвержден"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, не оплачен ли уже заказ
        if hasattr(order, 'payment') and order.payment.status == "paid":
            return Response({"error": "Заказ уже оплачен"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем платеж
        payment = Payment.objects.create(
            order=order,
            amount=order.total_cost,
            method=method,
            status="paid"
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
