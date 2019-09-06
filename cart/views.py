from django.shortcuts import render, redirect

from accounts.forms import LoginForm
from .models import Cart, Products
from order.models import Orders
from billing.models import BillingProfile


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'cart.html', context={'title': 'Cart', 'cart': cart_obj, 'new_obj': new_obj})


def cart_update(request):
    product_id = request.POST.get('product_id', None)
    if product_id:
        try:
            product_object = Products.objects.get(product_id=product_id)
            cart_obj, new_obj = Cart.objects.new_or_get(request)

            if product_object in cart_obj.products.all():
                cart_obj.products.remove(product_object)
            else:
                cart_obj.products.add(product_object)
            request.session['cart_items'] = cart_obj.products.count()
        except Products.DoesNotExist:
            return redirect('products:list')
    return redirect('cart:home')


def cart_checkout(request):
    cart_object, newly_created = Cart.objects.get_or_create(request)
    order_object = None
    if newly_created or cart_object.products.count() == 0:
        return redirect('cart:home')
    else:
        order_object, new_order_created = Orders.objects.get_or_create(cart=cart_object)
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    if user.is_authenticated:
        if user.email:
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(billing_profile_user=user,
                                                                                            billing_profile_email=user.email)
    context = {
            'order': order_object,
            'billing_profile': billing_profile,
            'login_form': login_form
    }
    return render(request, 'cart-checkout.html', context=context)
