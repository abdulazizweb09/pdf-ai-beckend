from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("male", "Erkak"),
        ("female", "Ayol"),
        ("other", "Boshqa"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("none", "Yo'q"),
        ("pending", "Kutilmoqda"),
        ("approved", "Tasdiqlangan"),
        ("rejected", "Rad etilgan"),
    ]

    SUBSCRIPTION_STATUS_CHOICES = [
        ("inactive", "Faol emas"),
        ("active", "Faol"),
        ("expired", "Muddati o'tgan"),
    ]

    # Asosiy fieldlar
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    telegram_username = models.CharField(max_length=100, blank=True)

    # Status fieldlar
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # To'lov / obuna fieldlari
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subscription_status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default="inactive"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="none"
    )
    access_until = models.DateTimeField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)

    # Vaqt
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.email