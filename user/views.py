from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"success": False, "message": message, "errors": errors}, status=status_code)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return success_response(
            "Ro'yxatdan muvaffaqiyatli o'tdingiz",
            data={
                "user": UserProfileSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return success_response(
            "Muvaffaqiyatli kirdingiz",
            data={
                "user": UserProfileSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return error_response("Refresh token kerak")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return error_response("Token noto'g'ri yoki allaqachon bekor qilingan")

        return success_response("Muvaffaqiyatli chiqdingiz")


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return success_response("Profil ma'lumotlari", data=serializer.data)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return error_response("Validatsiya xatosi", serializer.errors)

        serializer.save()
        return success_response(
            "Profil yangilandi",
            data=UserProfileSerializer(request.user).data,
        )