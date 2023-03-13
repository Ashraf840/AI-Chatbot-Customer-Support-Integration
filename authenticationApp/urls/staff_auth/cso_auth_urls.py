from django.urls import path
from ...views.staff_auth import (
    cso_auth_views  as cav,
)
from django.contrib.auth.views import LogoutView    # Concept: https://dev.to/codeitmichael/make-a-simple-employee-managing-app-in-django-with-class-based-views-with-login-logout-4fk7
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import warnings
from django.utils.deprecation import RemovedInDjango50Warning
from ...models import User_signin_token_tms



app_name = "cso_auth_urls"

# Extend "LogoutView" class-bsaed-view
class LogoutView_Custom(LogoutView):
    # def get(self, request, *args, **kwargs):
    #     print(request.user)
    #     print(request.user)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            # Delete User's signin token of TMS from the DB table ("User Signin Token (TMS)"). Firstly, check if there is any access-token record already in the db for removing, otherwise simply logout the user.
            # print(self.user)
            # print(request.user)
            # print(request.user.email)
            # print(request.user.username)
            user_email=request.user.email
            user_id=request.user.username
            try:
                User_signin_token_tms.objects.get(
                    user_email=user_email,
                    user_id=user_id,    
                ).delete()
            except User_signin_token_tms.DoesNotExist:
                pass
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
