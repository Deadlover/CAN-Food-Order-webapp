from django.urls import path
from . import views

urlpatterns = [
    path(r'menu',views.menupage,name='menu'),
    path(r'add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path(r'delete_order', views.deleteorder, name='delete-item'),
    path(r'updateitem', views.update_item, name='add'),
    path(r'delete_item', views.remove_item, name='delete'),
    path(r'cart', views.view_cart, name='cart'),
    path(r'menu/', views.search, name='search'),
    path('menu/<str:option>/', views.filter, name='filter'),
    path('menu/item/<int:foodid>/', views.fooddetail, name='detail'),
    path('review/', views.review, name='review'),
    path('esewacheckout/', views.esewacheckout, name='esewacheckout'),
    path('initiatekhalti/', views.Khalticheckout, name='initiatekhalti'),
    path('verifykhalti/', views.verifyKhalti, name='verifykhalti'),
]