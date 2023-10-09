from django.urls import path, include
from ..views import (
    password_reset_views as prv,
)

app_name = "authenticationApp"

urlpatterns = [
    # cso-auth
    path("cso-auth/", include(('authenticationApp.urls.staff_auth.cso_auth_urls', 'app_name'), namespace="CsoAuth")),
    # Password-Reset (First Time Login)
    path("initial-login/password-reset/<str:email>/", prv.PasswordResetView.as_view(), name="PasswordResetView"),
    # user-auth
    path("user-auth/", include(('authenticationApp.urls.user_auth.user_auth_urls', 'app_name'), namespace="UserAuth")),
    # User API
    path("user-auth/api/", include(('authenticationApp.api.user_api_urls', 'app_name'), namespace="UserAuthAPI")),
]