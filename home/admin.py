from django.contrib import admin
from .models import Fooditem,Category,Rating


# Register your models here.

@admin.register(Fooditem)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id','Name','quantity','price','active','image']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [ 'id','score','review','created_at','user','food_item']
    
@admin.register(Category)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name','description','id']



