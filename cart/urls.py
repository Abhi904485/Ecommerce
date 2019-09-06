from django.conf.urls import url
from .views import cart_home, cart_update, cart_checkout

app_name = 'cart'
urlpatterns = [
        url(r'^$', cart_home, name='home'),
        url(r'^update/$', cart_update, name='cart-update'),
        url(r'^checkout/$', cart_checkout, name='cart-checkout')
]
