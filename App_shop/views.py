from django.shortcuts import render

from django.views.generic import ListView, DetailView


from .models import Product

class Home(ListView):
    model = Product
    template_name = 'App_shop/home.html'


class Product_details(DetailView):
    model = Product
    template_name = 'App_shop/product_details.html'