from django.db import models
from django.conf import settings
from products.models import Products
from django.db.models.signals import m2m_changed, pre_save

User = settings.AUTH_USER_MODEL


# Create your models here.

class CartModelCustomQuerySet(models.query.QuerySet):
    def add_to_cart_queryset(self, user):
        user_obj = None
        if user:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(cart_user=user_obj)

    def get_by_id_queryset(self, cart_id):
        return self.model.objects.filter(cart_id=cart_id)

    def new_or_get_queryset(self, request):
        cart_id = request.session.get('cart_id', None)
        cart_query_set = self.get_by_id_queryset(cart_id)
        if cart_query_set.count() == 1:
            new_obj = False
            cart_obj = cart_query_set.first()
            if not cart_obj.cart_user and request.user.is_authenticated:
                cart_obj.cart_user = request.user
                cart_obj.save()
        else:
            cart_obj = self.add_to_cart_queryset(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.cart_id
        return cart_obj, new_obj

    # @staticmethod
    # def total_queryset(cart_object):
    #     products = cart_object.cart_product.all()
    #     total = 0
    #     for product in products:
    #         total += product.product_price
    #     cart_object.cart_total = total
    #     cart_object.save()


class CartModelManager(models.Manager):

    def get_query_set(self):
        return CartModelCustomQuerySet(self.model, using=self._db)

    def add_to_cart(self, user=None):
        return self.get_query_set().add_to_cart_queryset(user=user)

    def get_by_id(self, cart_id):
        return self.get_query_set().get_by_id_queryset(cart_id)

    def new_or_get(self, request):
        return self.get_query_set().new_or_get_queryset(request)

    # def total(self, cart_object):
    #     return self.get_query_set().total_queryset(cart_object=cart_object)


class Cart(models.Model):
    cart_user = models.ForeignKey(to=User, on_delete=models.CASCADE, help_text='Cart Foreign Key to user ', null=True,
                                  blank=True,
                                  error_messages={'required': 'please login with some user'},
                                  verbose_name='Cart User', db_column='cart_user')
    products = models.ManyToManyField(to=Products, verbose_name='cart products',
                                      help_text='Please choose some product',
                                      error_messages={'required': 'No product is selected'},
                                      db_column='products', blank=True)

    cart_id = models.AutoField(db_column='cart_id', verbose_name='cart id', help_text='this is cart primary key ',
                               error_messages={'required': 'Enter cart primary key'}, primary_key=True)
    cart_date_created = models.DateTimeField(verbose_name='date created date', auto_now_add=True,
                                             help_text="Please enter cart created Date", db_column='cart_date_created')
    cart_date_updated = models.DateTimeField(auto_now=True, verbose_name='Cart updated Date',
                                             help_text="Please enter cart updated Date", blank=True,
                                             null=True, db_column='cart_date_updated')
    cart_subtotal = models.DecimalField(verbose_name='cart subtotal', help_text="Subtotal of the cart",
                                        db_column='cart_subtotal',
                                        max_digits=10, default=0.00, decimal_places=2,
                                        error_messages={'required': 'cart subtotal missing'}, blank=False,
                                        null=False)
    cart_total = models.DecimalField(verbose_name='cart total', help_text="Total sum of the cart",
                                     db_column='cart_total',
                                     max_digits=10, default=0.00, decimal_places=2,
                                     error_messages={'required': 'Cart Total is missing'}, blank=False,
                                     null=False)

    def __str__(self):
        return "{}".format(self.cart_id)

    def __unicode__(self):
        return "{}".format(self.cart_id)

    objects = CartModelManager()

    class Meta:
        db_table = 'cart'
        verbose_name_plural = 'carts'
        default_manager_name = 'objects'


def m2m_cart_post_save_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        subtotal = 0
        for product in products:
            subtotal += product.product_price
        instance.cart_subtotal = subtotal
        instance.save()


m2m_changed.connect(m2m_cart_post_save_receiver, sender=Cart.products.through)


def cart_pre_save_total_receiver(sender, instance, *args, **kwargs):
    if instance.cart_subtotal > 0:
        instance.cart_total = instance.cart_subtotal
    else:
        instance.cart_subtotal = instance.cart_total = 0.00


pre_save.connect(cart_pre_save_total_receiver, sender=Cart)
