from django.urls import re_path, path
from .consumers import support_dashboard_consumer as sdc


websocket_urlpatterns = [
    # path('ws/cso-workload/support-dashboard/', sdc.SupportDashboardConsumer.as_asgi()),   # [OLD]
    path('ws/cso-workload/support-dashboard/<str:cso_mail>/', sdc.SupportDashboardConsumer.as_asgi()),
]


"""
Issue: After passes "@" through the channel-routing, the channel-group-name doesn't allow any special char (must be a valid unicode-string).
[Problem]: while trying to connect to the channel using the "SupportDashboardConsumer" consumer-class.
TypeError: Group name must be a valid unicode string with length < 100 containing only ASCII alphanumerics, hyphens, underscores, or periods, not chat_dashboard_enamulmajid021@gmail.com
"""
