from django.urls import path
from .import views

app_name='app_payment'

urlpatterns = [
    path('checkout/', views.Checkout, name='checkout'),
    path('pay/', views.Payment, name='payment'),
    path('status/', views.Complated, name='complate'),
    
]
  