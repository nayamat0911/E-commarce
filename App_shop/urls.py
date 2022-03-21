from django.urls import path
from .import views

app_name='app_shop'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('product/<pk>', views.Product_details.as_view(), name="product"),
]
