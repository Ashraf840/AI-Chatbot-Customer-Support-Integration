from django.urls import path
from ...views.staff_auth import (
    cso_auth_views  as cav,
)
from django.contrib.auth.views import LogoutView    # Concept: https://dev.to/codeitmichael/make-a-simple-employee-managing-app-in-django-with-class-based-views-with-login-logout-4fk7
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import warnings
from django.utils.deprecation import RemovedInDjango50Warning


app_name = "cso_auth_urls"

# Extend "LogoutView" class-bsaed-view
class LogoutView_Custom(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            # Delete User's signin token of TMS from the DB table ("User Signin Token (TMS)").

            warnings.warn(
                "Log out via GET requests is deprecated and will be removed in Django "
                "5.0. Use POST requests for logging out.",
                RemovedInDjango50Warning,
            )
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path("login/", cav.CSOLoginPageView.as_view(), name="CSOLoginPageView"),
    # path('logout/', LogoutView.as_view(next_page='authenticationApplication:CsoAuth:CSOLoginPageView'), name='CSOLogoutView'),
    path('logout/', LogoutView_Custom.as_view(
        next_page='authenticationApplication:CsoAuth:CSOLoginPageView'), name='CSOLogoutView'),
]
