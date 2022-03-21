
from django.urls import path
from .import views

app_name="app_login"

urlpatterns = [
    path('signup/', views.Create_account, name='signUp'),
    path('', views.User_login, name='login_user'),
    path('logout/', views.Logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),

]
