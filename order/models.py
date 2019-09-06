from django.db import models
from cart.models import Cart
from django.db.models.signals import pre_save, post_save
from Ecommerce.utils import unique_order_id_generator
from math import fsum


# Create your models here.

class Orders(models.Model):
    choices = (
            ('created', 'Created'),
            ('paid', 'Paid'),
            ('shipped', 'Shipped'),
            ('refunded', 'Refunded'),

    )
    order_id = models.CharField(max_length=120, verbose_name="Order ID", db_column="order_id",
                                help_text="Order id of order", error_messages={'required': 'Order_id is required'},
                                null=False, blank=True, unique=True
                                )
    cart = models.ForeignKey(verbose_name='Cart', to=Cart, on_delete=models.CASCADE, help_text="Foreign Key Cart",
                             error_messages={'required': 'Cart is required'}, blank=True, db_column='cart',
                             related_name='carts', related_query_name='cart'
                             )
    order_status = models.CharField(db_column='status', error_messages={'required': 'status is required'},
                                    verbose_name='Status', blank=False, null=False, max_length=120,
                                    help_text="status of order", choices=choices, default='created')

    order_shipping_total = models.DecimalField(verbose_name="Total Shipping Price",
                                               help_text="Total shipping price of Product",
                                               blank=False,
                                               null=False, default=100.00, max_digits=100, decimal_places=2,
                                               db_column='order_shipping_total',
                                               error_messages={'required': 'Order shipping total price  is required'}, )
    order_total = models.DecimalField(verbose_name="Total Price",
                                      help_text="Total price of Order",
                                      blank=False,
                                      null=False, default=0.00, max_digits=100, decimal_places=2,
                                      db_column='order_total',
                                      error_messages={'required': 'Order shipping total is required'}, )

    def __str__(self):
        return self.order_id

    def __unicode__(self):
        return self.order_id

    class Meta:
        db_table = "order"
        verbose_name_plural = "orders"

    def update_total(self):
        cart_total = self.cart.cart_total
        shipping_total = self.order_shipping_total
        new_total = fsum([cart_total, shipping_total])
        self.order_total = format(new_total, '.2f')
        self.save()
        return self.order_total


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(sender, instance, *args, **kwargs)


pre_save.connect(order_pre_save_receiver, sender=Orders)


def cart_post_save_total_receiver(sender, instance, created, *args, **kwargs):
    cart_object = instance
    cart_id = cart_object.cart_id
    query_set = Orders.objects.filter(cart__cart_id=cart_id)
    if query_set.count() == 1:
        order_object = query_set.first()
        order_object.update_total()


post_save.connect(cart_post_save_total_receiver, sender=Cart)


def order_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(order_post_save_receiver, sender=Orders)
