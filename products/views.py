from django.views.generic import ListView, DetailView

from .models import Products
from cart.models import Cart


# Create your views here.


class ProductListView(ListView):
    model = Products
    extra_context = {'title': 'Home'}


class ProductDetailSlugView(DetailView):
    model = Products
    extra_context = {'title': 'Detail'}
    slug_field = 'product_slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(**kwargs)
        cart_object, new_object = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_object
        return context
