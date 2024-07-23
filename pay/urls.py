from django.urls import path
from . import views

urlpatterns = [
    path('order_history/', views.history, name='orderhistory'),
    path('esewapayment/', views.esewapayment, name='esewa'),
    path('khalticheckout/', views.khalticheckout, name='khalti'),
    path('verifyKhalti/', views.verifyKhalti, name='verifykhalti'),
    path('order/', views.customerorderpage, name='order'),

]