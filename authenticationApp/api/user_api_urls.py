from django.urls import path
from . import (
    user_api_views as uav
    # UserDetailAPI as uda,
)

app_name = "user_api_urls"

urlpatterns = [
    path("user-detail/<str:email>/", uav.UserDetailAPI.as_view(), name="UserDetialAPI"),
]
