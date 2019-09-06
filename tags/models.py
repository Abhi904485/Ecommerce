from django.db import models

# Create your models here.
from products.models import Products
from django.db.models.signals import pre_save


from Ecommerce.utils import unique_slug_generator


class Tags(models.Model):
    tag_id = models.AutoField(error_messages={'required': 'tag id is required'}, null=False,
                              blank=False,
                              primary_key=True, db_column='tag_id', verbose_name='tag id',
                              help_text="primary key of tag table",
                              unique=True)

    tag_title = models.CharField(unique=True, default="Title", help_text="title of the tag",
                                 verbose_name="Title",
                                 db_column="tag_title", blank=False, null=False,
                                 error_messages={'required': 'tag title is required'}, max_length=100,
                                 )
    tag_description = models.CharField(default="Description of the tag", max_length=500,
                                       error_messages={'required': 'tag Description is required'},
                                       null=False,
                                       blank=False, db_column="tag_description",
                                       help_text="Description of the tag",
                                       verbose_name="tag description")

    tag_slug = models.SlugField(null=True, blank=True, help_text="Product slug field", db_column="tag_slug",
                                verbose_name="slug tag", error_messages={"required": "Enter the slug field"},
                                unique=True, )
    tag_active = models.BooleanField(default=False, db_column='tag_active', null=True, blank=True,
                                     help_text="Featured tag or not ", verbose_name="Featured Active",
                                     error_messages={"required": "Product Active required"})

    products = models.ManyToManyField(to=Products, related_name='tags', related_query_name='tag',
                                      db_column='product_tag', verbose_name='products',
                                      help_text='this is product tag')

    class Meta:
        db_table = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.tag_title


def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.tag_slug:
        instance.tag_slug = unique_slug_generator(sender, instance, *args, **kwargs)


pre_save.connect(tags_pre_save_receiver, sender=Tags)
