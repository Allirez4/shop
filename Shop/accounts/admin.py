from django.contrib import admin
from .forms import UserCreation, UserChange  # rename file to forms.py and update import if you can
from django.contrib.auth.admin import UserAdmin as baseadmin
from django.contrib.auth.models import Group
from .models import CustomUser,otp

class Useradmin(baseadmin):
    form = UserChange          # used on edit
    add_form = UserCreation     # used on add

    list_display = ('email', 'phone_number', 'full_name')
    list_filter = ('is_admin', 'is_active')  # must be tuple/list

    fieldsets = (
        (None, {
            'fields': ('email', 'phone_number', 'full_name', 'password'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_admin'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'full_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('full_name',)

admin.site.unregister(Group)
admin.site.register(CustomUser, Useradmin)
admin.site.register(otp)