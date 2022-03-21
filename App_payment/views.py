from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.

# models and forms
from .models import BillingAddress
from .forms import BillingForm
from App_order.models import Order

#for payment
import requests

from sslcommerz_python.payment import SSLCSession

from decimal import Decimal
import socket



from django.contrib.auth.decorators import login_required

@login_required

def Checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST , instance=saved_address)
        if form.is_valid():
            form.save()
            return redirect("app_payment:checkout")
        else:
            form = BillingForm(request.POST)
            messages.info(request, "Your address invaled")
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    order_items = order_qs[0].orderitem.all()
    order_total = order_qs[0].get_totals()

    check_context={
        "title":"checkout",
        "checkform":form,
        'order_items':order_items,
        'order_total':order_total,
        'saved_address':saved_address
    }
    return render(request,'App_payment/checkout.html',context=check_context)


# for payment
@login_required
def Payment(request):
    save_address = BillingAddress.objects.get_or_create(user=request.user)
    save_address = save_address[0]
    if not save_address.is_fully_filled():
        messages.info(request, f"Please complate shipping address")
        return redirect("app_payment:checkout")
        
    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please complate profile deatils!")
        return redirect("app_login:profile")

    # 1st step
    Store_ID= 'myweb621728f5e0c4d'
    API_Secret_Key = 'myweb621728f5e0c4d@ssl'

    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=Store_ID, sslc_store_pass=API_Secret_Key)

    #2nd step
    status_url = request.build_absolute_uri(reverse('app_payment:complate'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    #3rd step
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item = order_qs[0].orderitem.all()
    order_item_count = order_qs[0].orderitem.count()
    order_total = order_qs[0].get_totals()
    
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_item, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')
    
    # 4th step
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email  , address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    
    # 5th step
    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=save_address.address, city=save_address.city, postcode=save_address.zipcode, country=save_address.country)

    # 6th step
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])


@login_required
def Complated(request):
    return render(request,'App_payment/complate.html', context={})