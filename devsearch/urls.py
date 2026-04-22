from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, CustomSignupView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Override allauth's POST handlers
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),

    path("accounts/", include("allauth.urls")),
    path("", include("projects.urls")),
    path("", include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
