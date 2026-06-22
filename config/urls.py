from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from payments.urls import user_urlpatterns, admin_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("user.urls")),
    path("api/payments/", include((user_urlpatterns, "payments"))),
    path("api/admin/", include((admin_urlpatterns, "admin-payments"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)