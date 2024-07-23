from django.db import models
from django.conf import settings
from home.models import Fooditem
import uuid

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Fooditem, through="OrderItem")
    order_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    total_price = models.IntegerField()
    purchase_order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.first_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.Name} in Order #{self.order.pk}"
    

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    paymentid = models.CharField(max_length=100)

    def __str__(self):
        return f"Transaction {self.transaction_id} for Order #{self.order.pk}"