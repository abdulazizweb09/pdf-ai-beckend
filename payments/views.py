from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serilazers import (
    PaymentCreateSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentAdminSerializer,
    PaymentApproveRejectSerializer,
)
from user.permissions import IsAdminUser


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"success": False, "message": message, "errors": errors}, status=status_code)


class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        payment = serializer.save(user=request.user)
        return success_response(
            "To'lov so'rovi yuborildi. Admin tasdiqlashini kuting.",
            data=PaymentDetailSerializer(payment).data,
            status_code=status.HTTP_201_CREATED,
        )


class MyPaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentListSerializer(payments, many=True)
        return success_response("To'lovlaringiz", data=serializer.data)


class MyPaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk, user=request.user)
        except Payment.DoesNotExist:
            return error_response("To'lov topilmadi", status_code=status.HTTP_404_NOT_FOUND)

        serializer = PaymentDetailSerializer(payment)
        return success_response("To'lov tafsiloti", data=serializer.data)


# --- Admin views ---

class AdminPaymentListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        payments = Payment.objects.select_related("user").all()
        serializer = PaymentAdminSerializer(payments, many=True)
        return success_response("Barcha to'lovlar", data=serializer.data)


class AdminPaymentApproveView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.select_related("user").get(pk=pk)
        except Payment.DoesNotExist:
            return error_response("To'lov topilmadi", status_code=status.HTTP_404_NOT_FOUND)

        if payment.status == "approved":
            return error_response("Bu to'lov allaqachon tasdiqlangan")

        serializer = PaymentApproveRejectSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        # To'lovni yangilash
        payment.status = "approved"
        payment.approved_at = timezone.now()
        payment.admin_note = serializer.validated_data.get("admin_note", "")
        payment.save()

        # Foydalanuvchini yangilash
        user = payment.user
        user.is_premium = True
        user.payment_status = "approved"
        user.subscription_status = "active"

        if payment.duration_days:
            base = user.access_until if user.access_until and user.access_until > timezone.now() else timezone.now()
            user.access_until = base + timedelta(days=payment.duration_days)
        
        user.save()

        return success_response(
            "To'lov tasdiqlandi va foydalanuvchiga premium berildi",
            data=PaymentAdminSerializer(payment).data,
        )


class AdminPaymentRejectView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return error_response("To'lov topilmadi", status_code=status.HTTP_404_NOT_FOUND)

        if payment.status == "rejected":
            return error_response("Bu to'lov allaqachon rad etilgan")

        serializer = PaymentApproveRejectSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        payment.status = "rejected"
        payment.admin_note = serializer.validated_data.get("admin_note", "")
        payment.save()

        return success_response(
            "To'lov rad etildi",
            data=PaymentAdminSerializer(payment).data,
        )