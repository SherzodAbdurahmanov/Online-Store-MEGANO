from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32, default="pending")

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default="unpaid")
