from django.urls import re_path, path
from .consumers import support_dashboard_consumer as sdc


websocket_urlpatterns = [
    path('ws/cso-workload/support-dashboard/', sdc.SupportDashboardConsumer.as_asgi()),
]   