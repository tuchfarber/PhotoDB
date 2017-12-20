from django.contrib import admin

from .models import Photo, Tag, TagCategory

admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(TagCategory)
