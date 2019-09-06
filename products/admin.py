from django.contrib import admin

from .models import Products


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_slug']

    class Meta:
        model = Products


admin.site.register(Products, ProductAdmin)
