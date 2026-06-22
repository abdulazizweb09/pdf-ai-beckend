from django.urls import path
from .views import (
    PaymentCreateView,
    MyPaymentListView,
    MyPaymentDetailView,
    AdminPaymentListView,
    AdminPaymentApproveView,
    AdminPaymentRejectView,
)

user_urlpatterns = [
    path("create/", PaymentCreateView.as_view(), name="payment-create"),
    path("my/", MyPaymentListView.as_view(), name="my-payments"),
    path("my/<int:pk>/", MyPaymentDetailView.as_view(), name="my-payment-detail"),
]

admin_urlpatterns = [
    path("payments/", AdminPaymentListView.as_view(), name="admin-payments"),
    path("payments/<int:pk>/approve/", AdminPaymentApproveView.as_view(), name="admin-approve"),
    path("payments/<int:pk>/reject/", AdminPaymentRejectView.as_view(), name="admin-reject"),
]