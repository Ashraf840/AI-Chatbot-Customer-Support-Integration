from django.urls import path
from ...views.staff_auth import (
    cso_auth_views  as cav,
)
from django.contrib.auth.views import LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import warnings
from django.utils.deprecation import RemovedInDjango50Warning
from ...models import User_signin_token_tms
from home.models import CustomerSupportRequest
from staffApp.cso_connectivity_models import CSOOnline, CSOConnectedChannels


app_name = "cso_auth_urls"

class LogoutView_Custom(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            user_email=request.user.email
            user_id=request.user.username
            try:
                User_signin_token_tms.objects.get(
                    user_email=user_email,
                    user_id=user_id,    
                ).delete()
                try:
                    filtered_msg_reqs = CustomerSupportRequest.objects.filter(assigned_cso=user_email)
                    print(f"All msg requests of the CSO ({user_email}):", filtered_msg_reqs)
                    filtered_msg_reqs.delete()
                    print(f"All msg requests of the CSO ({user_email}):", filtered_msg_reqs)
                except:
                    pass
                try:
                    CSOConnectedChannels.objects.filter(cso_email=user_email).delete()
                    cso_online_instance = CSOOnline.objects.get(cso_email=user_email)
                    cso_online_instance.is_active = False
                    cso_online_instance.save()
                except:
                    pass
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
    path('logout/', LogoutView_Custom.as_view(
        next_page='authenticationApplication:CsoAuth:CSOLoginPageView'), name='CSOLogoutView'),
]
