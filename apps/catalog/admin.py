from django.contrib import admin
from django.utils.safestring import mark_safe

from api.v1.models.catalog import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_show', 'description', 'price', 'available', 'category', ]
    list_filter = ['name', 'price', 'category', ]

    def photo_show(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='60' />".format(obj.photo.url))
        return 'None'

    photo_show.__name__ = 'Фотография товара'
