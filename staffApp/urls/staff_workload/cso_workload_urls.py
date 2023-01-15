from django.urls import path
from ...views.cso_views import (
    cso_dashboard_views  as cdv,
)

app_name = "cso_workload_urls"

urlpatterns = [
    path("dashboard/", cdv.CsoDashboard.as_view(), name="CsoDashboard"),
]
