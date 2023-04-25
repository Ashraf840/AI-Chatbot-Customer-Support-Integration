from django.urls import path
from . import (
    user_api_views as uav,
    chat_room_create_api_views as crcav
)

app_name = "user_api_urls_chatbot_socket"

urlpatterns = [
    # user-detail-api
    # GET METHOD
    path("user-chatbot/socket/<str:chatbotSocketID>/", uav.UserDetailAPIChatbotSocket.as_view(), name="UserDetailAPIChatbotSocket"),
    # POST METHOD
    path("user-chatbot/socket/", uav.UserDetailAPIChatbotSocket.as_view(), name="UserDetailAPIChatbotSocket"),
    # auto-chatroom-create-api
    # POST METHOD
    path("user-chatroom/socket/", crcav.ChatRoomCreateAPISocket.as_view(), name="ChatRoomCreateAPISocket"),
]
