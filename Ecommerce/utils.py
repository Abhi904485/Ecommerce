from django.utils.text import slugify
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.ascii_uppercase):
    return "".join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(sender, instance, order_id=None, **kwargs):
    if order_id is not None:
        order_id = order_id
    else:
        order_id = random_string_generator()

    qs_exists = sender.objects.filter(order_id=order_id).exists()
    if qs_exists:
        order_id = "{order_id}{randstr}".format(
                order_id=order_id[0:6],
                randstr=random_string_generator(size=4)
        )
        return unique_order_id_generator(sender, instance, order_id, **kwargs)
    return order_id


def unique_slug_generator(sender, instance, new_slug=None, **kwargs):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.product_title)

    qs_exists = sender.objects.filter(product_slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                slug=slug,
                randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(sender, instance, new_slug, **kwargs)
    return slug
