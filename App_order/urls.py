from django.urls import path
from .import views

app_name='app_order'

urlpatterns = [
    path('add/<pk>', views.AddToCart, name='add_to_cart'),
    path('cart/', views.Cart_View, name='cart_item'),
    path('remove-cart/<pk>', views.remove_from_cart, name='remove'),
    path('increase/<pk>', views.Increase_item, name='increase'),
    path('decrease/<pk>', views.Decrease_item, name='decrease'),
]