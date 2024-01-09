from django.contrib import admin
from api.v1.models.cart import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
