from django.conf.urls import url

from products.views import (ProductListView, ProductDetailSlugView)

app_name = "products"
urlpatterns = [
        url(r'^$', ProductListView.as_view(), name='list', ),
        url(r'^(?P<product_slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),

]


