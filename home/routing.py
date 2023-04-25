from django.urls import re_path, path
from .consumers import (
    cso_visitor_chat_consumer as cvcc,
    chatbot_user_chat_consumer as cucc
)


websocket_urlpatterns = [
    path('ws/cso-visitor/chat-support/<str:room_slug>/', cvcc.CSOVisitorChatSuppportConsumer.as_asgi()),
    path('ws/user-chatbot/socket/<str:user_email>/', cucc.ChatbotUserChatConsumer.as_asgi()),
]