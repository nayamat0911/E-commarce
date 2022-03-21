from django.shortcuts import render, get_object_or_404, redirect

# authenticated
from django.contrib.auth.decorators import login_required

# models
from .models import Cart, Order
from App_shop.models import Product
# messages
from django.contrib import messages

@login_required
def AddToCart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased= False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("app_order:cart_item")
        else:
            order.orderitem.add(order_item[0])
            messages.info(request, "This item was added to your cart")
            return redirect("app_shop:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitem.add(order_item[0])
        messages.info(request,"this item was added to your cart.")
        return redirect("app_shop:home")
    

@login_required
def Cart_View(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_order/cart.html', context={'carts':carts, 'order':order})

    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('app_shop:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(item=item).exists():
            order_item= Cart.objects.filter(item=item,user=request.user, purchased=False)[0]
            order.orderitem.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your Cart")
            return redirect('app_order:cart_item')

        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("app_shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("app_shop:home")


@login_required
def Increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("app_order:cart_item")
        else:
            messages.info(request, f"{item.name} is not in yout cart")
            return redirect('app_shop:home')
    else:
        messages.info(request, "You don't have active order")
        return redirect("app_shop:home")


@login_required
def Decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect('app_order:cart_item')
            else:
                order.orderitem.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart.")
                return redirect("app_shop:home")

        else:
            messages.info(request, f"{item.name} is not in yout cart")
            return redirect('app_shop:home')
    else:
        messages.info(request, "You don't have active order")
        return redirect("app_shop:home")
    
