from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
from home.models import CustomerSupportRequest
from channels.layers import get_channel_layer



# Customer Support Dashboard Consumer
class CSOOnlineConnectivityConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(CSOOnlineConnectivityConsumer, self).__init__(*args, **kwargs)
        self.room_group_name = None

    
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: CSOOnlineConnectivityConsumer")
        self.room_group_name = 'cso_online_connectivity_dashboard'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        async_to_sync(self.accept())
        print("#"*50)

    def receive(self):
        print("#"*50)
        print("[recieve() method] Recieved data to backend consumer class: CSOOnlineConnectivityConsumer")
        print("#"*50)
    
    # Custom method: send all new support-req from the db-signal's (home.signals.customer_support_request_signal) channel-group-send method.
    def cso_online_connectivity(self, event):
        connectivity_report_email = event['connectivity_report_email']
        connectivity_report_room_slug = event['connectivity_report_room_slug']
        connectivity_status = event['connectivity_status']
        # connectivity_report_online = 'online' if event['connectivity_report_online'] else 'offline'
        connectivity_report_online = event['connectivity_report_online']

        print("\n"*3)
        print("$"*50)
        print(f"instance cso_email (sent from the signal): {connectivity_report_email}")
        print(f"instance cso_email data-type: {type(connectivity_report_email)}")
        print(f"instance room_slug (sent from the signal): {connectivity_report_room_slug}")
        print(f"instance room_slug data-type: {type(connectivity_report_room_slug)}")
        print(f"instance connectivity_status (sent from the signal): {connectivity_status}")
        print(f"instance connectivity_status data-type: {type(connectivity_status)}")
        print(f"instance connectivity_report_online (sent from the signal): {connectivity_report_online}")
        print(f"instance connectivity_report_online data-type: {type(connectivity_report_online)}")
        print("$"*50)
        print("\n"*3)

        self.send(text_data=json.dumps({
            'connectivity_report_email': connectivity_report_email,
            'connectivity_report_room_slug': connectivity_report_room_slug,
            'connectivity_report_online': connectivity_report_online,
            'connectivity_status': connectivity_status,
        }))
    
    def disconnect(self, *args, **kwargs):
        print("#"*50)
        print("[disconnect() method] Recieved data to backend consumer class: CSOOnlineConnectivityConsumer")
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("#"*50)