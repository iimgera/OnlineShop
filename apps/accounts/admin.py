from django.contrib import admin
from api.v1.models.accounts import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
