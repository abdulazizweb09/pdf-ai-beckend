from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user", "amount", "payment_method",
        "transaction_id", "status", "created_at", "approved_at",
    ]
    list_filter = ["status", "payment_method", "created_at"]
    search_fields = ["user__email", "transaction_id"]
    readonly_fields = ["created_at", "updated_at", "approved_at"]
    ordering = ["-created_at"]