from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse


# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout , authenticate

# import forms
from .forms import SignUpForm, ProfileForm

# import models
from .models import Profile

# massages
from django.contrib import messages


# Create your views here.
def Create_account(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return HttpResponseRedirect(reverse('app_login:login_user'))

    sign__form_cont={
        'title':"Sign Up",
        'signup_form':form
    }
    return render(request, "App_login/singup.html", context=sign__form_cont)


def User_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('app_login:profile'))


    return render(request, 'App_login/login.html', context={'form':form})

@login_required
def Logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out!")
    return HttpResponseRedirect(reverse("app_login:login_user"))


@login_required
def profile(request):
    current_user=request.user
    chang_form = ProfileForm(instance=current_user)
    if request.method == "POST":
        chang_form = ProfileForm(request.POST, instance=current_user)
        if chang_form.is_valid():
            chang_form.save()
            # chang_form = ProfileForm(instance=current_user)
            messages.success(request,"your Profile has been Updated!")
            return HttpResponseRedirect(reverse('app_payment:complate'))

    change_form_con={
        "title":"change Profile",
        'change_form':chang_form
    }
    return render(request, "App_login/change_profile.html", context=change_form_con)




