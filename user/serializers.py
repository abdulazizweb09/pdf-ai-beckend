from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password_confirm", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username band.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Parollar mos kelmadi."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Email yoki parol noto'g'ri.")
        if not user.is_active:
            raise serializers.ValidationError("Akkaunt bloklangan.")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "phone_number", "avatar", "bio", "date_of_birth", "gender",
            "country", "city", "address", "telegram_username",
            "is_verified", "is_premium", "subscription_status",
            "payment_status", "access_until", "created_at",
        ]
        read_only_fields = [
            "id", "email", "is_verified", "is_premium",
            "subscription_status", "payment_status", "access_until", "created_at",
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "phone_number", "avatar",
            "bio", "date_of_birth", "gender", "country",
            "city", "address", "telegram_username",
        ]