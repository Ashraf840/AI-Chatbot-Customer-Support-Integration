from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import UserChatbotSocket



def save_user_chatbot_socket(user_email, chatbot_socket_id, registered_user_session_uuid):
    user_chatbot_socket = UserChatbotSocket.objects.filter(user_email=user_email).delete()
    user_chatbot_socket = UserChatbotSocket.objects.create(
        user_email=user_email,
        chatbot_socket_id=chatbot_socket_id,
        registered_user_session_uuid=registered_user_session_uuid
    )
    print("Created a new user-chatbot-socket record!", user_chatbot_socket)
    return user_chatbot_socket


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
        self.room_name_normalized="".join(ch for ch in self.room_name if ch.isalnum())
        self.room_group_name = 'user_chatbot_socket_%s' % self.room_name_normalized
        print(f"room-group name: {self.room_group_name}")
        print(f'Channel name: {self.channel_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.accept())
        print("#"*50)

    def receive(self, text_data=None, bytes_data=None):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: ChatbotUserChatConsumer")
        data = json.loads(text_data)
        if 'ChatbotUserSocketStorage' in data:
            user_email = data['user_email']
            chatbot_socket_id = data['chatbot_socket_id']
            registered_user_session_uuid = data['registered_user_session_uuid']
            u_chatbot_socket = async_to_sync(save_user_chatbot_socket(
                    user_email=user_email,
                    chatbot_socket_id=chatbot_socket_id,
                    registered_user_session_uuid=registered_user_session_uuid
                ))
        print("#"*50)
    

    def auto_create_chatroom(self, event):
        user_email = event['user_email']
        chatbot_socket_id = event['chatbot_socket_id']
        issuerOid = event['issuerOid']
        self.send(text_data=json.dumps({
            'auto_create_chatroom': 'True',
            'user_email': user_email,
            'chatbot_socket_id': chatbot_socket_id,
            'issuerOid': issuerOid,
        }))

    def disconnect(self, *args, **kwargs):
        print("#"*50)
        
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: ChatbotUserChatConsumer")
        print("#"*50)
