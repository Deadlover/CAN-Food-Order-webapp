from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage,name='Loginpage'),
    path('signup',views.SignupPage,name='Signup'),
    path('logout/', views.LogoutPage,name='logout'),
]