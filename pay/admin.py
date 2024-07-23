from django.contrib import admin
from .models import Order,OrderItem,Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','order_date','is_complete','is_paid','total_price','purchase_order_id']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','food_item','quantity']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','status','timestamp','amount','transaction_id','order']