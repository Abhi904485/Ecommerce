from django.contrib import admin
from .models import Tags


# Register your models here.

class TagsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'tag_slug']


admin.site.register(Tags, TagsAdmin)
