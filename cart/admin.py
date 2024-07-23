from django.contrib import admin
from .models import Cart,CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart','food_item','quantity']