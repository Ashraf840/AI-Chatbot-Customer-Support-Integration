from django.urls import path
from ...views.user_auth import (
    user_auth_views  as uav,
)
from django.contrib.auth.views import LogoutView

app_name = "user_auth_urls"

urlpatterns = [
    path("login/", uav.UserLoginPageView.as_view(), name="UserLoginPageView"),
    path('logout/', LogoutView.as_view(next_page='authenticationApplication:UserAuth:UserLoginPageView'), name='UserLogoutView'),
]
