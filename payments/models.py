from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("approved", "Tasdiqlangan"),
        ("rejected", "Rad etilgan"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("click", "Click"),
        ("payme", "Payme"),
        ("card", "Karta"),
        ("cash", "Naqd"),
        ("other", "Boshqa"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=255, unique=True)
    screenshot = models.ImageField(upload_to="payment_screenshots/", null=True, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)
    plan_name = models.CharField(max_length=100, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.status}"