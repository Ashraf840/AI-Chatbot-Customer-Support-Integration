from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
from home.models import CustomerSupportRequest
from channels.layers import get_channel_layer


# Customer Support Dashboard Consumer
class SupportDashboardConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(SupportDashboardConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
    
    # [Default method] Create an asynchronous connection-function
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: SupportDashboardConsumer")
        # self.room_name = 'dashboard'
        # self.room_group_name = 'chat_%s' % self.room_name
        self.room_name = self.scope['url_route']['kwargs']['cso_mail']
        room_name_normalized="".join(ch for ch in self.room_name if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        self.room_group_name = 'chat_dashboard_%s' % room_name_normalized    # THIS pattern is required to sent any asynchrobous msg to this consumer-channel
        print(f"room-group name: {self.room_group_name}")
        # self.user_obj = self.scope['user']
        # print(f"Newly Connected (username): {self.user_obj.username}")
        print(f'Channel name: {self.channel_name}')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        async_to_sync(self.accept())

        # get all the customer-support-requests using the staticmethod of "CustomerSupportRequest" model
        all_support_reqs = CustomerSupportRequest.get_customer_support_reqs()
        print(f"All support reqs: {all_support_reqs}")

        # what is get_channel_layer?????
        channel_layer_var = get_channel_layer()
        print(f"channel_layer_var: {channel_layer_var}")

        # Send to the single specific CSO to his/her dashboard websocket; who connects to this consumer currently
        self.send(text_data=json.dumps({
            'status': 'Backend Consumer (Websocket): Connected - initial hit from frontend - then conn payload sent from backend',
            'payload': 'Any kind of python object payload is sent to frontend WebSocket onmessage() method',
            'payload2': f'{all_support_reqs}',
        }))
        print("#"*50)

    # Default method of "WebsocketConsumer" class
    # Receive the msg from frontend & broadcast it to the entire channel
    def receive(self, text_data=None, bytes_data=None):
        print("#"*50)
        print("[recieve() method] Recieved data to backend consumer class: SupportDashboardConsumer")
        print("#"*50)
    
    # Custom method: send all new support-req from the db-signal's (home.signals.customer_support_request_signal) channel-group-send method.
    def new_support_req(self, event):
        new_supprt_reqst = event['new_support_request']
        self.send(text_data=json.dumps({
            'new_supprt_reqst': new_supprt_reqst,
        }))

    # Default method of "WebsocketConsumer" class
    def disconnect(self, *args, **kwargs):
        print("#"*50)
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: SupportDashboardConsumer")
        print("#"*50)
