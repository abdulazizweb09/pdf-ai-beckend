from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "email", "username", "first_name", "last_name",
        "is_staff", "is_active", "is_verified", "is_premium",
        "payment_status", "created_at",
    ]
    list_filter = ["is_staff", "is_active", "is_verified", "is_premium", "payment_status"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Shaxsiy ma'lumotlar", {"fields": (
            "username", "first_name", "last_name", "phone_number",
            "avatar", "bio", "date_of_birth", "gender",
            "country", "city", "address", "telegram_username",
        )}),
        ("Huquqlar", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified", "groups", "user_permissions")}),
        ("To'lov / Obuna", {"fields": ("is_premium", "payment_status", "subscription_status", "access_until", "balance")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )