from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .models import Customer


class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
        "get_customer"
    )
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    readonly_fields = ("last_login", "date_joined")

    list_filter = []

    def get_customer(self, obj):
        return obj.customer.id if hasattr(obj, "customer") else "No Customer"
    
    get_customer.short_description = "Customer ID"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "phone_number", "country")
    search_fields = ("user__email", "user__username", "first_name", "last_name")
    ordering = ("user__email",)



admin.site.register(Customer, CustomerAdmin)
admin.site.register(User, UserAdmin)
