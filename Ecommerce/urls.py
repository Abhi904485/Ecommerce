"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Ecommerce import settings
from .views import (about_page, contact_page, login_page, register_page, logout_page, )

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^about/$', about_page, name='about'),
        url(r'^contact/$', contact_page, name='contact'),
        url(r'^login/$', login_page, name='login'),
        url(r'^logout/$', logout_page, name='logout'),
        url(r'^register/$', register_page, name='register'),
        url(r'^products/', include('products.urls', namespace='products'), ),
        url(r'^search/', include('search.urls', namespace='search'), ),
        url(r'^cart/', include('cart.urls', namespace='cart'), ),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
