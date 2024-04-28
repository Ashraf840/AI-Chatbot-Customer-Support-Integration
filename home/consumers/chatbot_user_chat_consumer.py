from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import UserChatbotSocket
import requests


# [Static Method]: Store chat msg into DB
def save_user_chatbot_socket(user_email, chatbot_socket_id, registered_user_session_uuid):
    # Check if there is any record based on "chatbot_socket_id" in the "UserChatbotSocket" model, if None, then create a new record,
    # user_chatbot_socket = UserChatbotSocket.objects.filter(chatbot_socket_id=chatbot_socket_id, registered_user_session_uuid= registered_user_session_uuid)
    # user_chatbot_socket = UserChatbotSocket.objects.filter(chatbot_socket_id=chatbot_socket_id)
    user_chatbot_socket = UserChatbotSocket.objects.filter(user_email=user_email).delete()
    user_chatbot_socket = UserChatbotSocket.objects.create(
        user_email=user_email,
        chatbot_socket_id=chatbot_socket_id,
        registered_user_session_uuid=registered_user_session_uuid
    )
    print("Created a new user-chatbot-socket record!", user_chatbot_socket)
    # if len(user_chatbot_socket) == 0:
    return user_chatbot_socket


# Customer Support Visitor Chat Consumer
class ChatbotUserChatConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super(ChatbotUserChatConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room_name_normalized = None
    
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: ChatbotUserChatConsumer")
        self.room_name = self.scope['url_route']['kwargs']['user_email']
        self.room_name_normalized="".join(ch for ch in self.room_name if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        self.room_group_name = 'user_chatbot_socket_%s' % self.room_name_normalized     # THIS pattern is required to sent any asynchrobous msg to this consumer-channel
        print(f"room-group name: {self.room_group_name}")
        print(f'Channel name: {self.channel_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        async_to_sync(self.accept())
        print("#"*50)

    def receive(self, text_data=None, bytes_data=None):
        # [explaination]: mitigate filling up the db by spam-intruder in the cs-chat-page (those wo manually create a cs-chat-page to pupolate the db without asking for support to a CSO though chatbot).
        # check if the visitor is not a spam-intruder
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: ChatbotUserChatConsumer")
        data = json.loads(text_data)
        if 'ChatbotUserSocketStorage' in data:
            # print('Automatically hitting for storing user-email & socket-id!')
            user_email = data['user_email']
            chatbot_socket_id = data['chatbot_socket_id']
            registered_user_session_uuid = data['registered_user_session_uuid']
            # print("User email:", user_email)
            # print("User chatbot socket id:", chatbot_socket_id)
            # print("User session uuid:", registered_user_session_uuid)
            # store user-email & socket-id into the db-table ("UserChatbotSocket")
            u_chatbot_socket = async_to_sync(save_user_chatbot_socket(
                    user_email=user_email,
                    chatbot_socket_id=chatbot_socket_id,
                    registered_user_session_uuid=registered_user_session_uuid
                ))
            # print(f"Saved msg: {u_chatbot_socket.awaitable.created_at}")
        
        if 'prompt_chatroom_create' in data:
            print("Make a post request to 'chat_room_create_api_view' api! Reqire additional information!")
            user_email = data['user_email']
            chatbot_socket_id = data['chatbot_socket_id']
            issuerOid = data['issuerOid']

            user_organization = data['user_organization']
            location = data['location']
            district = data['district']
            division = data['division']
            # print(f"user_email; {user_email}; chatbot_socket_id: {chatbot_socket_id}; issuerOid: {issuerOid}\
            #       user_organization; {user_organization}; location: {location}; district: {district}; division: {division}")

            # url = "http://172.16.6.91:80/home/api/user-chatroom/socket/"
            url = "http://127.0.0.1:8080/home/api/user-chatroom/socket/"
            
            payload = json.dumps({
                "user_email": user_email,
                "chatbot_socket_id": chatbot_socket_id,
                "issuerOid": issuerOid,

                "user_organization": user_organization,
                "location": location,
                "district": district,
                "division": division,
            })
            headers = {
            'Content-Type': 'application/json'
            }
            
            requests.post(
                url, payload,
                headers= headers
            )


        print("#"*50)
    

    def auto_create_chatroom(self, event):
        print("auto_create_chatroom chatroom is called!")

        user_email = event['user_email']
        chatbot_socket_id = event['chatbot_socket_id']
        issuerOid = event['issuerOid']
        self.send(text_data=json.dumps({
            'auto_create_chatroom': 'True',
            'user_email': user_email,
            'chatbot_socket_id': chatbot_socket_id,
            'issuerOid': issuerOid,
        }))

    def prompt_chatroom_create(self, event):
        user_email = event['user_email']
        chatbot_socket_id = event['chatbot_socket_id']
        issuerOid = event['issuerOid']
        user_organization = event['user_organization']
        location = event['location']
        district = event['district']
        division = event['division']

        self.send(text_data=json.dumps({
            'prompt_chatroom_create': 'True',
            'user_email': user_email,
            'chatbot_socket_id': chatbot_socket_id,
            'issuerOid': issuerOid,
            'user_organization': user_organization,
            'location': location,
            'district': district,
            'division': division,
        }))

    def disconnect(self, *args, **kwargs):
        print("#"*50)
        
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: ChatbotUserChatConsumer")
        print("#"*50)
