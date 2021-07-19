from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'user_type',
        'date_joined'
    )
    list_filter = (
        'user_type',
        'date_joined'
    )
