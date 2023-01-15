from django.urls import path
from ...views.staff_auth import (
    cso_auth_views  as cav,
)
from django.contrib.auth.views import LogoutView    # Concept: https://dev.to/codeitmichael/make-a-simple-employee-managing-app-in-django-with-class-based-views-with-login-logout-4fk7

app_name = "cso_auth_urls"

urlpatterns = [
    path("login/", cav.CSOLoginPageView.as_view(), name="CSOLoginPageView"),
    path('logout/', LogoutView.as_view(next_page='authenticationApplication:CsoAuth:CSOLoginPageView'), name='CSOLogoutView'),
]
