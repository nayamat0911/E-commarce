from django.contrib import admin
from django.urls import path,include

#input for media files
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_login.urls')),
    path('', include('App_shop.urls')),
    path('order/', include('App_order.urls')),
    path('payment/', include('App_payment.urls')),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)