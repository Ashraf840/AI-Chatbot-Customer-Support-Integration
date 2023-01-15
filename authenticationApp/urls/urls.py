from django.urls import path, include
from ..views import (
    password_reset_views as prv,
)

app_name = "authenticationApp"

urlpatterns = [
    path("cso-auth/", include(('authenticationApp.urls.staff_auth.cso_auth_urls', 'app_name'), namespace="CsoAuth")),
    # Password-Reset (First Time Login)
    # TODO: Pass email as extra param in the URI.
    path("initial-login/password-reset/<str:email>/", prv.PasswordResetView.as_view(), name="PasswordResetView"),
]