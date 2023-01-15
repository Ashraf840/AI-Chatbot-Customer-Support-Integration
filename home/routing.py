from django.urls import re_path, path
from .consumers import cso_visitor_chat_consumer as cvcc


websocket_urlpatterns = [
    path('ws/cso-visitor/chat-support/<str:room_slug>/', cvcc.CSOVisitorChatSuppportConsumer.as_asgi()),
]