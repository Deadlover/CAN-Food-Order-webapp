from django.urls import path
from . import views

urlpatterns = [
    path(r'home',views.homepage,name='Home'),
    path(r'upload',views.uploadpage,name='upload'),
    path(r'foodupload',views.fooduploadpage,name='foodupload'),
    path(r'categoryupload',views.categoryuploadpage,name='categoryupload'),
    path(r'edit',views.editmenupage,name='editmenu'),
    path(r'update/<int:food_id>',views.update,name='edit'),
    path(r'delete/<int:food_id>',views.Delete,name='delete'),
    path(r'contact',views.contactpage,name='contact'),
    path('Customer_review/', views.commentPage, name='Customer_review'),
    path('Setting/<str:Whatchange>', views.Settingpage, name='UserSetting'),
]