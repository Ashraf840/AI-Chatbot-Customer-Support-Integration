from django.urls import path
from ...views.cso_views import (
    cso_dashboard_views  as cdv,
)

app_name = "cso_workload_urls"

urlpatterns = [
    path("cso-dashboard/", cdv.CsoDashboard.as_view(), name="CsoDashboard"),
    path("support-dashboard/<str:email>/", cdv.SupportDashboard.as_view(), name="SupportDashboard"),
    path("support-dashboardNew/<str:email>/", cdv.SupportDashboardNew.as_view(), name="SupportDashboardNew"),

    path("cso-online-connectivity-dashboard/", cdv.CSOOnlineConnectivityDashboard.as_view(), name="CSOOnlineConnectivityDashboard"),
]
