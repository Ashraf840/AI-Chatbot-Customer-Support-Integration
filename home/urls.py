from django.urls import path
from .views import (
    home_views as hmvs,
    chatBot_resp_views as chbtrspvs,
)

app_name = "homeApp"

urlpatterns = [
    path("", hmvs.LangingPage.as_view(), name="LangingPage"),
    path("bot-resp/", chbtrspvs.bot_resp, name="bot_resp"),
    path("customer-support-request/", hmvs.CustomerSupportReq.as_view(), name="CustomerSupportRequest"),
    path("customer-support/<str:room_slug>/", hmvs.CustomerSupportRoom.as_view(), name="CustomerSupportRoom"),
]