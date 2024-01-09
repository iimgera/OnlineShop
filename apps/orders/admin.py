from django.contrib import admin
from api.v1.models.orders import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass