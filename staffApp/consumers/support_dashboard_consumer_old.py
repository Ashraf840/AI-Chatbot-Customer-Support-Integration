from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
import json
from home.models import CustomerSupportRequest
from channels.layers import get_channel_layer
from ..cso_connectivity_models import CSOOnline, CSOConnectedChannels
from authenticationApp.utils.userDetail import UserDetail
from .utils.appendLocationBasedData import AppendLocationBasedData



def create_channel_conn(room_slug, channel_name, cso_email):
    print('*'*10, "create_channel_conn() func is called")
    print("room slug:", room_slug)
    channel_name = channel_name.replace('specific.', '')  # remove the prefix from each channel-name before storing into the db
    print("channel name:", channel_name)
    print("cso email:", cso_email)
    print('create channel-record of cso-user using email in the "CSOConnectedChannels" model.')
    CSOConnectedChannels.objects.create(
        cso_email=cso_email,
        room_slug=room_slug,
        channel_value=channel_name
    )

def remove_channel_conn(room_slug, channel_name, cso_email):
    print('*'*10, "remove_channel_conn() func is called")
    print("room slug:", room_slug)
    channel_name = channel_name.replace('specific.', '')  # remove the prefix from each channel-name before storing into the db
    print("channel name:", channel_name)
    print("cso email:", cso_email)
    print('[first check if exist] remove channel-record of cso from the "CSOConnectedChannels" model.')
    try:
        CSOConnectedChannels.objects.get(
            cso_email=cso_email,
            room_slug=room_slug,
            channel_value=channel_name
        ).delete()
    except CSOConnectedChannels.DoesNotExist:
        print('No such active channel exists!')

def append_loc_based_data(
        user:object,
        user_organization:str,
        user_location:str,
        user_district:str,
        user_division:str,
    ):
    AppendLocationBasedData(user, user_organization, user_location, user_district, user_division)


def make_user_online(
        user: object,
        user_organization: str,
        user_location: str,
        user_district: str,
        user_division: str
    ):

    if user.user_organization is None \
        or user.location is None \
        or user.district is None \
        or user.division is None:
        # print("user organization, location, district or division any of this None")

        append_loc_based_data(
            user,
            user_organization,
            user_location,
            user_district,
            user_division,
        )

    if not user.is_active:
        user.is_active = True
        user.save()


def make_user_offline(
        user: object,
        user_organization: str,
        user_location: str,
        user_district: str,
        user_division: str
    ):
    if user.user_organization is None \
        or user.location is None \
        or user.district is None \
        or user.division is None:
        # print("user organization, location, district or division any of this None")

        append_loc_based_data(
            user, 
            user_organization,
            user_location,
            user_district,
            user_division,
        )
    
    # Check if the user's active; then change it to False
    if user.is_active:
        user.is_active = False
        user.save()



def active_user_online(
        room_slug, channel_name, cso_email,
        user_organization: str,
        user_location:str,
        user_district:str,
        user_division:str):
    try:
        cso_online_obj = CSOOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
        make_user_online(
            cso_online_obj,
            user_organization,
            user_location,
            user_district,
            user_division
        )
        create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
    except CSOOnline.DoesNotExist:
        cso_online_obj = CSOOnline.objects.create(
            cso_email=cso_email, 
            room_slug=room_slug,
            user_organization=user_organization,
            location=user_location,
            district=user_district,
            division=user_division
        )
        create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)



def count_active_channel(room_slug, cso_email):
    return CSOConnectedChannels.objects.filter(
        cso_email=cso_email,
        room_slug=room_slug
    )

def deactive_user_online(
        room_slug, channel_name, cso_email,
        user_organization: str,
        user_location:str,
        user_district:str,
        user_division:str):
    try:
        cso_online_obj = CSOOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
        remove_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
        total_active_channel = count_active_channel(room_slug=room_slug, cso_email=cso_email)
        if len(total_active_channel) == 0:
            make_user_offline(
                cso_online_obj,
                user_organization,
                user_location,
                user_district,
                user_division
            )
            CSOConnectedChannels.objects.filter(cso_email=cso_email).delete()
    except CSOOnline.DoesNotExist:
        print('CSO doesn\'t exist to make the CSO offline!')


# Customer Support Dashboard Consumer
class SupportDashboardConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(SupportDashboardConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_name_normalized = None
        self.room_group_name = None
        self.user_obj = None
    
    # [Default method] Create an asynchronous connection-function
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['cso_mail']
        self.room_name_normalized="".join(ch for ch in self.room_name if ch.isalnum())
        self.room_group_name = 'chat_dashboard_%s' % self.room_name_normalized
        self.user_obj = self.scope['user']

        usr_detail = UserDetail(user_email=self.room_name)
        usr_profile = usr_detail.user_profile_detail()
        user_organization, user_location, user_district, user_division = usr_profile.user_organization, usr_profile.location, usr_profile.district, usr_profile.division

        async_to_sync(active_user_online(
            cso_email=self.user_obj.email, 
            room_slug=self.room_name_normalized, 
            channel_name=self.channel_name,
            
            user_organization=user_organization,
            user_location=user_location,
            user_district=user_district,
            user_division=user_division
        ))

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.accept())

        all_support_reqs = CustomerSupportRequest.get_customer_support_reqs()

        channel_layer_var = get_channel_layer()

        # Send to the single specific CSO to his/her dashboard websocket; who connects to this consumer currently
        self.send(text_data=json.dumps({
            'status': 'Backend Consumer (Websocket): Connected - initial hit from frontend - then conn payload sent from backend',
            'payload': 'Any kind of python object payload is sent to frontend WebSocket onmessage() method',
            'payload2': f'{all_support_reqs}',
        }))
        print("#"*50)
    
    def new_support_req(self, event):
        new_supprt_reqst = event['new_support_request']
        self.send(text_data=json.dumps({
            'new_supprt_reqst': new_supprt_reqst,
        }))
    
    def old_support_req_resolved(self, event):
        old_supprt_req_roomSlug = event['instance_room_slug']
        old_supprt_req_isResolved = event['instance_resolved']
        total_current_reqs = event['total_current_reqs']
        print('\n'*3)
        print('+'*50)
        print('Old support request is resolved (from SupportDashboardConsumer consumer)!')
        print('+'*50)
        print('\n'*3)
        self.send(text_data=json.dumps({
            'old_supprt_req_roomSlug': old_supprt_req_roomSlug,
            'old_supprt_req_isResolved': old_supprt_req_isResolved,
            'total_current_reqs': total_current_reqs,
        }))

    def old_support_req_dismissed(self, event):
        old_supprt_req_roomSlug = event['instance_room_slug']
        old_supprt_req_isDismissed = event['instance_dismissed']
        total_current_reqs = event['total_current_reqs']
        print('\n'*3)
        print('+'*50)
        print('Old support request is dismissed (from SupportDashboardConsumer consumer)!')
        print('+'*50)
        print('\n'*3)
        self.send(text_data=json.dumps({
            'old_supprt_req_roomSlug': old_supprt_req_roomSlug,
            'old_supprt_req_isDismissed': old_supprt_req_isDismissed,
            'total_current_reqs': total_current_reqs,
        }))
    

    # Custom method: send the chat-convo-cancelled-by-user to the frontend of the specific CSO's email.
    def support_req_chat_convo_cancelled(self, event):
        instance_room_slug = event['instance_room_slug']
        # old_supprt_req_isResolved = event['instance_resolved']
        total_current_reqs_after_convo_cancelled = event['total_current_reqs_after_convo_cancelled']
        print('\n'*3)
        print('+'*50)
        print('Chat convo is cancelled (from SupportDashboardConsumer consumer)!')
        print('+'*50)
        print('\n'*3)
        self.send(text_data=json.dumps({
            'chat_convo_cancelled': 'True',
            'instance_room_slug': instance_room_slug,
            'total_current_reqs_after_convo_cancelled': total_current_reqs_after_convo_cancelled,
        }))

    # Default method of "WebsocketConsumer" class
    def disconnect(self, *args, **kwargs):
        print("#"*50)

        usr_detail = UserDetail(user_email=self.room_name)
        usr_profile = usr_detail.user_profile_detail()
        user_organization, user_location, user_district, user_division = usr_profile.user_organization, usr_profile.location, usr_profile.district, usr_profile.division
       
        async_to_sync(deactive_user_online(
            cso_email=self.user_obj.email, 
            room_slug=self.room_name_normalized, 
            channel_name=self.channel_name,

            user_organization=user_organization,
            user_location=user_location,
            user_district=user_district,
            user_division=user_division
        ))

        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: SupportDashboardConsumer")
        print("#"*50)
