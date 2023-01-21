from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import CSOVisitorMessage, CustomerSupportRequest
from ..user_connectivity_models import ChatSupportUserOnline


def make_user_online(user):
    # Check if the user's active; otherwise change it to True
    if not user.is_active:
        user.is_active = True
        user.save()

def make_user_offline(user):
    # Check if the user's active; then change it to False
    if user.is_active:
        user.is_active = False
        user.save()


def active_user_online(room_slug, cso_email=None, visitor_session_uuid=None):
    """
    This func is responsible for creating new record in the "ChatSupportUserOnline" model if no record found of the user based on certain condition.
    """
    print("active_user_online() func is called")
    print("room slug:", room_slug)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('check cso-user online using email in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
            print('Found active cso user record!', user_online_obj)
            # Make the user online if it's not online by passing the "user_online_obj" entirely, so that the follwing func doesn't require to query the "ChatSupportUserOnline" model before making the user online
            make_user_online(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            user_online_obj = ChatSupportUserOnline.objects.create(cso_email=cso_email, room_slug=room_slug)
            print('Created a active cso user record!', user_online_obj)
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('check visitor-user online using session-uuid in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Found active visitor user record!', user_online_obj)
            # Make the user online if it's not online by passing the "user_online_obj" entirely, so that the follwing func doesn't require to query the "ChatSupportUserOnline" model before making the user online
            make_user_online(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            user_online_obj = ChatSupportUserOnline.objects.create(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Created a active visitor user record!', user_online_obj)


def deactive_user_online(room_slug, cso_email=None, visitor_session_uuid=None):
    """
    This func is responsible for deactive old user in the "ChatSupportUserOnline" model based on certain condition.
    """
    print("deactive_user_online() func is called")
    print("room slug:", room_slug)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('check cso-user online using email in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
            print('Intially make the user (cso) offline!', user_online_obj)
            # Make the user offline if it's online by passing the "user_online_obj" entirely, so that the follwing func doesn't require to query the "ChatSupportUserOnline" model before making the user offline.
            make_user_offline(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            print('User doesn\'t exist to make the user offline!')
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('check visitor-user online using session-uuid in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Intially make the user (visitor) offline!', user_online_obj)
            # Make the user offline if it's online by passing the "user_online_obj" entirely, so that the follwing func doesn't require to query the "ChatSupportUserOnline" model before making the user offline.
            make_user_offline(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            print('User (visitor) doesn\'t exist to make the user offline!')


# [Static Method]: Store chat msg into DB
def save_message(message, user_identity, room_slug):
    msg = CSOVisitorMessage.objects.create(
        message=message,
        user_identity=user_identity, 
        room_slug=room_slug
    )
    return msg


# Customer Support Visitor Chat Consumer
class CSOVisitorChatSuppportConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(CSOVisitorChatSuppportConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.is_visitor_intruder = False
        self.user_obj = None
        self.visitor_session_uuid = None
    
    # [Default method] Create an asynchronous connection-function
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: CSOVisitorChatSuppportConsumer")
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_obj = self.scope['user']
        print(f'Channel name: {self.channel_name}')

        # First check if the connection is created by a CSO-user or by a visitor
        # print('user object id:', self.user_obj.id)
        if self.user_obj.id is not None:
            print('Check if the cso-user exists in the "ChatSupportUserOnline" table; if not found, then create a record in that table & later create channel record of the cso-user! (both "ChatSupportUserOnline" & "ChatSupportUserConnectedChannels" tables use cso-email)')
            # call the "active_user_online()" func here for storing CSO's email in the user-online-active model
            async_to_sync(active_user_online(cso_email=self.user_obj.email, room_slug=self.room_name))
        else:
            # Get the [VISITOR'S SESSION UUID] from the "CustomerSupportRequest" model using the room_slug.
            # Try-catch block to mitigate intruders trying to create chat-room (using manual input in the browser's URL) without requesting for customerSupport through the chatbot.
            visitor_support_req = CustomerSupportRequest.objects.filter(
                room_slug=self.room_name,
            ).order_by('-created_at')
            # print(visitor_support_req)
            # Check if the queryset is empty
            if visitor_support_req:
                self.visitor_session_uuid = visitor_support_req[0].visitor_session_uuid
                print('visitor session uuid:', self.visitor_session_uuid)
                print('check if there is any record with the "visitor_session_uuid", if not found any then create a record in "ChatSupportUserOnline" table & later create channel of the visitor-user! (both "ChatSupportUserOnline" & "ChatSupportUserConnectedChannels" tables use visitor-session-uuid)')
                # call the "active_user_online()" func here for storing visitor's session in the user-online-active model
                async_to_sync(active_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name))
            else:
                # [explaination]: mitigate filling up the 'chat-msg' db by spam-intruders in the cs-chat-page (those wo manually create a cs-chat-page to pupolate the db without asking for support to a CSO though chatbot).
                self.is_visitor_intruder = True



        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        async_to_sync(self.accept())
        print("#"*50)

    # Default method of "WebsocketConsumer" class
    # Receive the msg from frontend & broadcast it to the entire channel
    def receive(self, text_data=None, bytes_data=None):
        # [explaination]: mitigate filling up the db by spam-intruder in the cs-chat-page (those wo manually create a cs-chat-page to pupolate the db without asking for support to a CSO though chatbot).
        # check if the visitor is not a spam-intruder
        if not self.is_visitor_intruder:
            print("#"*50)
            data = json.loads(text_data)  # decode json-stringified data into python-dict
            # print(data)
            message = data['message']
            user_identity = data['user_identity']
            roomslug = data['roomslug']
            # print(message)
            # print(user_identity)
            # print(roomslug)

            # before sending the msg to the channel-group, store the msg into db
            msg = async_to_sync(save_message(
                message=message,
                user_identity=user_identity,
                room_slug=roomslug
            ))
            print(f"Saved msg: {msg.awaitable.created_at}")

            # Send the data to all the channels in the group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                # pass a dictionary with custom key-value pairs
                {
                    'type': 'chat_message',  # will be used to call as a method
                    'message': message,
                    'user_identity': user_identity,
                    'roomslug': roomslug,
                }
            )
            print("[recieve() method] Recieved data to backend consumer class: CSOVisitorChatSuppportConsumer")
            print("#"*50)
        else:
            self.send(text_data=json.dumps({
                'intruder_redirection': 'Redirect the intruder to homepage!',
            }))
            # Disconnect the intruder's channel conn without saving his msg to db
            self.disconnect(self)
    
    # This method will be called in the receive-method while sending msg to channel-group.
    # "event" param contains other keys (except 'type' key) from inside the dictionary passed as param in "channel_layer.group_send"
    def chat_message(self, event):
        message = event['message']
        user_identity = event['user_identity']
        roomslug = event['roomslug']
        # Send to the room in the frontend; send in a json-format; send func responsible for sending data to frontend
        # Send to the single specific client's chatting platform websocket; who connects to this consumer currently
        self.send(text_data=json.dumps({
            'message': message,
            'user_identity': user_identity,
            'roomslug': roomslug,
        }))

    # Default method of "WebsocketConsumer" class
    def disconnect(self, *args, **kwargs):
        print("#"*50)
        if self.user_obj.id is not None:
            print('(CSO is about to disconnect!) Make query in the "ChatSupportUserOnline" model using cso-email, if found make the user offline!')
            # call the deactive_user_online() func
            async_to_sync(deactive_user_online(cso_email=self.user_obj.email, room_slug=self.room_name))
        
        if self.visitor_session_uuid is not None:
            print('(Visitor is about to disconnect!) Make query in the "ChatSupportUserOnline" model using visitor_session_uuid, if found make the user offline!')
            # call the deactive_user_online() func
            async_to_sync(deactive_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name))

        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: CSOVisitorChatSuppportConsumer")
        print("#"*50)
