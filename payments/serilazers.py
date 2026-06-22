from rest_framework import serializers
from .models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "amount", "payment_method", "transaction_id",
            "screenshot", "comment", "plan_name", "duration_days",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Summa 0 dan katta bo'lishi kerak.")
        return value

    def validate_transaction_id(self, value):
        if Payment.objects.filter(transaction_id=value).exists():
            raise serializers.ValidationError("Bu transaction ID allaqachon ishlatilgan.")
        return value


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "amount", "payment_method", "transaction_id",
            "status", "plan_name", "created_at", "approved_at",
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "user_email", "amount", "payment_method",
            "transaction_id", "screenshot", "comment", "status",
            "admin_note", "plan_name", "duration_days",
            "created_at", "updated_at", "approved_at",
        ]


class PaymentApproveRejectSerializer(serializers.Serializer):
    admin_note = serializers.CharField(required=False, allow_blank=True)