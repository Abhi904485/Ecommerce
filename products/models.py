import os
import random

from django.db.models import Q
from django.db.models.signals import pre_save
from django.db import models
from Ecommerce.utils import unique_slug_generator
from django.shortcuts import reverse


class ProductCustomQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(product_active=True)

    def featured(self):
        return self.filter(product_featured=True, active=True)

    def search(self, query):
        lookups = Q(product_title__icontains=query) | Q(product_description__icontains=query) | Q(
                product_price__icontains=query) | Q(tag__tag_title__icontains=query) | Q(
                tag__tag_description__icontains=query)
        return self.active().filter(lookups).distinct()


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductCustomQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id1):
        qs = self.get_queryset().filter(product_id=id1, product_active=True)
        if qs:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


def upload_image_path(instance, filename):
    random_folder_name = random.randint(1, 126871632781832)
    random_file_name = "{}{}".format(random_folder_name, os.path.splitext(os.path.basename(filename))[1])
    return os.path.join("products", str(random_folder_name), random_file_name)


class Products(models.Model):
    product_id = models.AutoField(error_messages={'required': 'product id is required'}, null=False,
                                  blank=False,
                                  primary_key=True, db_column='product_id', verbose_name='product id',
                                  help_text="primary key of product table",
                                  unique=True)

    product_title = models.CharField(unique=True, default="Title", help_text="title of the product",
                                     verbose_name="Title",
                                     db_column="product_title", blank=False, null=False,
                                     error_messages={'required': 'product title is required'}, max_length=100,
                                     )
    product_description = models.CharField(default="Description of the product", max_length=500,
                                           error_messages={'required': 'product Description is required'},
                                           null=False,
                                           blank=False, db_column="product_description",
                                           help_text="Description of the product",
                                           verbose_name="product description")
    product_price = models.DecimalField(verbose_name="Product price", help_text="price of the product",
                                        blank=False,
                                        null=False, default=0.00, max_digits=10, decimal_places=2,
                                        db_column='product_price',
                                        error_messages={'required': 'product Price is required'}, )
    product_image = models.ImageField(verbose_name="image name", null=False, blank=False,
                                      help_text="image of the product", db_column='product_image',
                                      error_messages={'required': 'please upload product image'},
                                      default="default.jpg", upload_to=upload_image_path)

    product_slug = models.SlugField(null=True, blank=True, help_text="Product slug field", db_column="product_slug",
                                    verbose_name="slug product", error_messages={"required": "Enter the slug field"},
                                    unique=True, )

    product_featured = models.BooleanField(default=False, db_column='product_featured', null=True, blank=True,
                                           help_text="Featured product or not ", verbose_name="Featured Product",
                                           error_messages={"required": "Product Featured required"})
    product_active = models.BooleanField(default=False, db_column='product_active', null=True, blank=True,
                                         help_text="Featured product or not ", verbose_name="Featured Active",
                                         error_messages={"required": "Product Active required"})

    objects = ProductManager()

    class Meta:
        db_table = "product"
        verbose_name_plural = "products"
        default_related_name = "product"
        default_manager_name = "objects"

    def __str__(self):
        return self.product_title

    def __unicode__(self):
        return self.product_title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'product_slug': self.product_slug})

    @property
    def name(self):
        return self.product_title


def products_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = unique_slug_generator(sender, instance, *args, **kwargs)


pre_save.connect(products_pre_save_receiver, sender=Products)
