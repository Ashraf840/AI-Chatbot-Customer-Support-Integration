from django.urls import re_path, path
from .consumers import cso_dashboard_consumer as cdc


websocket_urlpatterns = [
    path('ws/cso-workload/dashboard/', cdc.CSODashboardConsumer.as_asgi()),
]