from django.urls import path, include
from .views import (
    home_views as hmvs,
    chatBot_resp_views as chbtrspvs,
)

app_name = "homeApp"

urlpatterns = [
    path("", hmvs.LangingPage.as_view(), name="LangingPage"),
    path("customer-support-request/", hmvs.CustomerSupportReq.as_view(), name="CustomerSupportRequest"),
    path("customer-support/<str:room_slug>/", hmvs.CustomerSupportRoom.as_view(), name="CustomerSupportRoom"),
    path("home/api/", include(('home.api.api_urls', 'app_name'), namespace="HomeAppAPI")),
]