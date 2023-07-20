from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mvisuals.models import Product, Category, DeliveryInformation, Order, CustomUser, MyCart
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ("category",)
class CategoryAdmin(admin.ModelAdmin):
    pass

class DeliveryInformationAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class MyCartAdmin(admin.ModelAdmin):
    pass


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.user_roles)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role',)

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'role', )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('role',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('User Roles', {
            'fields': ('role',)
        })
    )
    add_form = CustomUserCreationForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MyCart, MyCartAdmin)
admin.site.register(DeliveryInformation, DeliveryInformationAdmin)

