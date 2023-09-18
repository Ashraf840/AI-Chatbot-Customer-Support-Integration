from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import CSOVisitorMessage, CustomerSupportRequest, CSOVisitorConvoInfo, RemarkResolution
from ..user_connectivity_models import ChatSupportUserOnline, ChatSupportUserConnectedChannels


def create_channel_conn(room_slug, channel_name, cso_email=None, visitor_session_uuid=None):
    print('*'*10, "create_channel_conn() func is called")
    print("room slug:", room_slug)
    channel_name = channel_name.replace('specific.', '')  # remove the prefix from each channel-name before storing into the db
    print("channel name:", channel_name)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('create channel-record of cso-user using email in the "ChatSupportUserConnectedChannels" model.')
        ChatSupportUserConnectedChannels.objects.create(
            cso_email=cso_email,
            room_slug=room_slug,
            channel_value=channel_name
        )
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('create channel-record of visitor using visitor_session_uuid in the "ChatSupportUserConnectedChannels" model.')
        ChatSupportUserConnectedChannels.objects.create(
            visitor_session_uuid=visitor_session_uuid,
            room_slug=room_slug,
            channel_value=channel_name
        )

def remove_channel_conn(room_slug, channel_name, cso_email=None, visitor_session_uuid=None):
    print('*'*10, "remove_channel_conn() func is called")
    print("room slug:", room_slug)
    channel_name = channel_name.replace('specific.', '')  # remove the prefix from each channel-name before storing into the db
    print("channel name:", channel_name)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('[first check if exist] remove channel-record of cso-user from the "ChatSupportUserConnectedChannels" model.')
        try:
            ChatSupportUserConnectedChannels.objects.get(
                cso_email=cso_email,
                room_slug=room_slug,
                channel_value=channel_name
            ).delete()
        except ChatSupportUserConnectedChannels.DoesNotExist:
            print('No such active channel exists!')
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('[first check if exist] remove channel-record of visitor from the "ChatSupportUserConnectedChannels" model.')
        try:
            ChatSupportUserConnectedChannels.objects.get(
                visitor_session_uuid=visitor_session_uuid,
                room_slug=room_slug,
                channel_value=channel_name
            ).delete()
        except ChatSupportUserConnectedChannels.DoesNotExist:
            print('No such active channel exists!')
    

# Can make a common function (used in "staffApp/consumers/support_dashboard_consumer.py")
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


def active_user_online(room_slug, channel_name, cso_email=None, visitor_session_uuid=None):
    """
    This func is responsible for creating new record in the "ChatSupportUserOnline" model if no record found of the user based on certain condition.
    """
    print('*'*10, "active_user_online() func is called")
    print("room slug:", room_slug)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('check cso-user online using email in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
            print('Found active cso user record!', user_online_obj)
            # Make the user online if it's not online by passing the "user_online_obj" entirely, so that the following func doesn't require to query the "ChatSupportUserOnline" model before making the user online
            make_user_online(user_online_obj)
            # Create multiple channels of the same user to track that users -online-status regardless of creating duplicate multiple tabs.
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
        except ChatSupportUserOnline.DoesNotExist:
            # Create user online record
            user_online_obj = ChatSupportUserOnline.objects.create(cso_email=cso_email, room_slug=room_slug)
            print('Created a active cso user record!', user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('check visitor-user online using session-uuid in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Found active visitor user record!', user_online_obj)
            # Make the user online if it's not online by passing the "user_online_obj" entirely, so that the follwing func doesn't require to query the "ChatSupportUserOnline" model before making the user online
            make_user_online(user_online_obj)
            # Create multiple channels of the same user to track that users -online-status regardless of creating duplicate multiple tabs.
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)
        except ChatSupportUserOnline.DoesNotExist:
            # Create user online record
            user_online_obj = ChatSupportUserOnline.objects.create(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Created a active visitor user record!', user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)


def count_active_channel(room_slug, cso_email=None, visitor_session_uuid=None):
    # filter-search using both (cso-email/visitor-session-uuid) and room-slug
    print('*'*10, "count_active_channel() func is called")
    if cso_email is not None:
        return ChatSupportUserConnectedChannels.objects.filter(
            cso_email=cso_email,
            room_slug=room_slug
        )
    
    if visitor_session_uuid is not None:
        return ChatSupportUserConnectedChannels.objects.filter(
            visitor_session_uuid=visitor_session_uuid,
            room_slug=room_slug
        )


def deactive_user_online(room_slug, channel_name, cso_email=None, visitor_session_uuid=None):
    """
    This func is responsible for deactivating the old user in the "ChatSupportUserOnline" model based on certain condition.
    """
    print('*'*10, "deactive_user_online() func is called")
    print("room slug:", room_slug)
    if cso_email is not None:
        print("cso email:", cso_email)
        print('check cso-user online using email in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(cso_email=cso_email, room_slug=room_slug)
            print('Intially make the user (cso) offline!', user_online_obj)
            # Remove the exisiting active channel(s) of the same user(CSO) for each "Screen-refresh"/"Duplicate-tab-creation"
            remove_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
            total_active_channel = count_active_channel(room_slug=room_slug, cso_email=cso_email)
            print('total_active_channel (cso):', total_active_channel)
            # [INITIAL-STEP, later firstly check if the total opened channel of that individual user is 0 before making the user's status offline] 
            if len(total_active_channel) == 0:
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
            # Remove the exisiting active channel(s) of the same user(Visitor) for each "Screen-refresh"/"Duplicate-tab-creation"
            remove_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)
            total_active_channel = count_active_channel(room_slug=room_slug, visitor_session_uuid=visitor_session_uuid)
            print('total_active_channel (visitor):', total_active_channel)
            # [INITIAL-STEP, later firstly check if the total opened channel of that individual user is 0 before making the user's status offline]
            if len(total_active_channel) == 0:
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
            async_to_sync(active_user_online(cso_email=self.user_obj.email, room_slug=self.room_name, channel_name=self.channel_name))
        else:
            # Get the [VISITOR'S SESSION UUID] from the "CustomerSupportRequest" model using the room_slug.
            # Try-catch block to mitigate intruders trying to create chat-room (using manual input in the browser's URL) without requesting for customerSupport through the chatbot.
            visitor_support_req = CustomerSupportRequest.objects.filter(
                room_slug=self.room_name,
            ).order_by('-created_at')
            # print(visitor_support_req)
            # Check if the queryset is empty
            if visitor_support_req:
                # [Edge-case]: if a new visitor with the same room-slug enters into the room, s/he will get the access of the room.
                self.visitor_session_uuid = visitor_support_req[0].visitor_session_uuid
                print('visitor session uuid:', self.visitor_session_uuid)
                print('check if there is any record with the "visitor_session_uuid", if not found any then create a record in "ChatSupportUserOnline" table & later create channel of the visitor-user! (both "ChatSupportUserOnline" & "ChatSupportUserConnectedChannels" tables use visitor-session-uuid)')
                # call the "active_user_online()" func here for storing visitor's session in the user-online-active model
                async_to_sync(active_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name, channel_name=self.channel_name))
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

            # For CSO & registered visitors messaging-block
            if 'message' in data:
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

            # if 'support_is_resolved' in data:
            #     # TODO: Make the "CSOVisitorConvoInfo" record as resolved.
            #     cso_email = data['cso_email']
            #     reg_user_email = data['reg_user_email']
            #     room_slug = data['roomslug']
            #     remark_input_resolve_value = data['remark_input_resolve_value']

            #     # cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=room_slug, cso_email=cso_email)  # mark the convo-info as resolved, & make the CSO disconnected from the conversation
            #     # cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug)
                
            #     # # if (not cso_visitor_convo_info.is_resolved) and cso_visitor_convo_info.is_connected:
                    
            #     # cso_visitor_convo_info.is_resolved, cso_visitor_convo_info.is_connected = True, False
            #     # cso_visitor_convo_info.save()

            #     # RemarkResolution.objects.create(
            #     #     cso_user_convo=cso_visitor_convo_info,
            #     #     remarks=remark_input_resolve_value
            #     # )

            #     # if not cust_support_req.is_resolved:
            #     #     cust_support_req.is_resolved = True
            #     #     cust_support_req.save()
                
            #     # async_to_sync(self.channel_layer.group_send)(
            #     #     self.room_group_name,
            #     #     # pass a dictionary with custom key-value pairs
            #     #     {
            #     #         'type': 'support_resolved',  # will be used to call as a method
            #     #         'cso_email': cso_email,
            #     #         'reg_user_email': reg_user_email,
            #     #     }
            #     # )
                
            #     # print('The conversation is marked as resolved!')
            
            if 'cso_user_convo_cancelled' in data:
                cso_email = data['cso_email']
                reg_user_email = data['reg_user_email']
                room_slug = data['roomslug']
                print('The conversation is cancelled by the user!')
                print("User email:", reg_user_email)
                print("CSO email:", cso_email)

                # TODO: Backend logics related to db
                cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=room_slug)  # mark the convo-info as resolved, & make the CSO disconnected from the conversation
                cso_visitor_convo_info.is_cancelled, cso_visitor_convo_info.is_connected = True, False
                cso_visitor_convo_info.save()

                # Delete the message request in the CSR dashboard
                cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug).delete()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'chat_convo_cancelled',  # will be used to call as a method
                        'cso_email': cso_email,
                        'reg_user_email': reg_user_email,
                        'room_slug': room_slug,
                    }
                )

            # if 'cso_user_convo_dismissed' in data:
            #     remark_value = data['remark_input_dismiss_value']
            #     cso_email = data['cso_email']
            #     reg_user_email = data['reg_user_email']
            #     room_slug = data['roomslug']
            #     print('The conversation is dismissed by the CSO!')
            #     print("User email:", reg_user_email)
            #     print("CSO email:", cso_email)
            #     print("Room Slug:", room_slug)
            #     print("Remarks:", remark_value)

            #     # # # TODO: Backend logics related to db
            #     cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=room_slug)  # mark the convo-info as resolved, & make the CSO disconnected from the conversation
            #     print(f"cso_visitor_convo_info: {cso_visitor_convo_info.room_slug} --- {cso_visitor_convo_info.is_dismissed} --- {cso_visitor_convo_info.is_resolved}")
            #     cso_visitor_convo_info.is_dismissed, cso_visitor_convo_info.is_connected = True, False
            #     cso_visitor_convo_info.save()

            #     RemarkResolution.objects.create(
            #         cso_user_convo=cso_visitor_convo_info,
            #         remarks=remark_value
            #     )

            #     # Delete the message request in the CSR dashboard
            #     # cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug).delete()
            #     cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug)
            #     print(f"Deleting the customer-support-request: {cust_support_req.room_slug} --- {cust_support_req.registered_user_email_normalized} --- {cust_support_req.assigned_cso}")
            #     cust_support_req.delete()

            #     async_to_sync(self.channel_layer.group_send)(
            #         self.room_group_name,
            #         # pass a dictionary with custom key-value pairs
            #         {
            #             'type': 'chat_convo_dismissed',  # will be used to call as a method
            #             'cso_email': cso_email,
            #             'reg_user_email': reg_user_email,
            #             'room_slug': room_slug,
            #         }
            #     )

            # Human Feedback
            if 'feedback' in data:
                feedback = data['feedback']
                roomslug = data['roomslug']
                # print(f'feedback: {feedback}')
                # print(f'roomslug: {roomslug}')

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'human_feedback',  # will be used to call as a method
                        'feedback': feedback,
                        'roomslug': roomslug,
                    }
                )
            
            # Multiline Reply Mode
            if 'mlr' in data:
                mlr = data['mlr']
                roomslug = data['roomslug']
                # print(f'Multiline Reply Mode: {mlr}')
                # print(f'roomslug: {roomslug}')
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'multiline_reply_mode',  # will be used to call as a method
                        'mlr': mlr,
                        'roomslug': roomslug,
                    }
                )
            
            # Send HF on MLR mode disble
            if 'sendHfOnMlrDisable' in data and data['sendHfOnMlrDisable']=='Send HF on MLR mode disble':
                print("Sent socket signal to chatroom to send HF to customer end; since HDO has disabled the MLR mode!")
                user_identity = data['user_identity']
                roomslug = data['roomslug']
                # print(f'User Identity (Send HF on MLR disabled): {user_identity}')
                # print(f'roomslug: {roomslug}')
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'send_hf_on_mlr_disable',  # will be used to call as a method
                        'user_identity': user_identity,
                        'roomslug': roomslug,
                    }
                )
            
            # Conversational Reply mode
            if 'cr' in data:
                cr = data['cr']
                roomslug = data['roomslug']
                # print(f'Conversational Reply Mode: {cr}')
                # print(f'roomslug: {roomslug}')
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'conversational_reply_mode',  # will be used to call as a method
                        'cr': cr,
                        'roomslug': roomslug,
                    }
                )
            
            # Send HF on CR mode disble
            if 'sendHfOnCrDisable' in data and data['sendHfOnCrDisable']=='Send HF on CR mode disble':
                print("Sent socket signal to chatroom to send HF to customer end; since HDO has disabled the CR mode!")
                user_identity = data['user_identity']
                roomslug = data['roomslug']
                # print(f'User Identity (Send HF on CR disabled): {user_identity}')
                # print(f'roomslug: {roomslug}')
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'send_hf_on_cr_disable',  # will be used to call as a method
                        'user_identity': user_identity,
                        'roomslug': roomslug,
                    }
                )

            # HDO query mode
            if 'hifq' in data:
                # hifq = human input field query
                # print("HIFQ is sent to backend:", data['hifq'])
                # print("Roomslug (hifq):", data['roomslug'])
                hifq = data['hifq']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    # pass a dictionary with custom key-value pairs
                    {
                        'type': 'query_reply_mode',  # will be used to call as a method
                        'hifq': hifq,
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
    
    # [Custom Method] This method will be called in the receive-method while sending msg to channel-group.
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


    # [Custom Method] To get the signal of the support is resolved from the "views\home_views.py" file's post-method of "CustomerSupportRoom" class-view
    def support_resolved(self, event):
        cso_email = event['cso_email']
        reg_user_email = event['reg_user_email']
        ticket_issue_oid = event['ticket_issue_oid']    # not necessary
        user_signing_token_tms = event['user_signing_token_tms']    # not necessary
        remark_input_resolve_value = event['remark_input_resolve_value']
        roomSlugParam = event['roomSlugParam']
        print('\n', '-'*50)
        print('The support is resolved')
        print("ticket_issue_oid:", ticket_issue_oid)    # not necessary
        print("user_signing_token_tms:", user_signing_token_tms)    # not necessary
        print("remark_input_resolve_value:", remark_input_resolve_value)
        print("cso_email:", cso_email)
        print("reg_user_email:", reg_user_email)
        print("roomSlugParam:", roomSlugParam)
        print('\n', '-'*50)


        # cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=roomSlugParam, cso_email=cso_email)  # mark the convo-info as resolved & make the CSO disconnected from the conversation
        # cust_support_req = CustomerSupportRequest.objects.get(room_slug=roomSlugParam)
        
        # RemarkResolution.objects.create(
        #     cso_user_convo=cso_visitor_convo_info,
        #     remarks=remark_input_resolve_value
        # )
        
        # # if (not cso_visitor_convo_info.is_resolved) and cso_visitor_convo_info.is_connected:
        
        # cso_visitor_convo_info.is_resolved, cso_visitor_convo_info.is_connected = True, False
        # cso_visitor_convo_info.save()

        # if not cust_support_req.is_resolved:
        #     cust_support_req.is_resolved = True
        #     cust_support_req.save()

        print('The conversation is marked as resolved!')

        self.send(text_data=json.dumps({
            'support_is_resolved': 'The support is resolved!',
            'cso_email': cso_email,
            'reg_user_email': reg_user_email,
        }))
    

    def support_request_cleared(self, event):
        print('\n', '-'*50)
        print('The support request is cleared!')
        print('\n', '-'*50)
        CSOVisitorConvoInfo_isCancelled = event['CSOVisitorConvoInfo_isCancelled']
        print(f"CSOVisitorConvoInfo_isCancelled: {CSOVisitorConvoInfo_isCancelled}")
        # reg_user_email = event['reg_user_email']
        # Check & send custom signal of clearing support-req if the chat-convo-is-cancelled
        if (CSOVisitorConvoInfo_isCancelled):
            self.send(text_data=json.dumps({
                'support_req_is_removed': 'The support request is removed!',
                'CSOVisitorConvoInfo_isCancelled': CSOVisitorConvoInfo_isCancelled
            }))

    
    def chat_convo_cancelled(self, event):
        print('\n', '-'*50)
        print('The chat conversation is cancelled by the user!')
        print('\n', '-'*50)
        cso_email = event['cso_email']
        reg_user_email = event['reg_user_email']
        room_slug = event['room_slug']
        self.send(text_data=json.dumps({
            'conversation_is_cancelled': 'True',
            'cso_email': cso_email,
            'reg_user_email': reg_user_email,
            'room_slug': room_slug,
        }))
    
    def chat_convo_dismissed(self, event):
        common_cso_email = event['common_cso_email']
        common_registered_user_email = event['common_registered_user_email']
        # ticket_issue_oid = event['ticket_issue_oid']
        # user_signing_token_tms = event['user_signing_token_tms']
        remark_input_dismiss_value = event['remark_input_dismiss_value']
        roomSlugParam = event['roomSlugParam']

        print('\n', '-'*50)
        print('The chat conversation is dismissed by the user!')
        print("common_cso_email:", common_cso_email)
        print("common_registered_user_email:", common_registered_user_email)
        # print("ticket_issue_oid:", ticket_issue_oid)
        # print("user_signing_token_tms:", user_signing_token_tms)
        print("remark_input_dismiss_value:", remark_input_dismiss_value)
        print("roomSlugParam:", roomSlugParam)
        print('\n', '-'*50)


        # cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=roomSlugParam, cso_email=common_cso_email)  # mark the convo-info as dismissed & make the CSO disconnected from the conversation
        # cust_support_req = CustomerSupportRequest.objects.get(room_slug=roomSlugParam)
        
        # RemarkResolution.objects.create(
        #     cso_user_convo=cso_visitor_convo_info,
        #     remarks=remark_input_dismiss_value
        # )

        # cso_visitor_convo_info.is_dismissed, cso_visitor_convo_info.is_connected = True, False
        # cso_visitor_convo_info.save()


        # **************************** Define similar to "issue-resolve" func: "cust_support_req.is_dismissed" (new attribute to "cust_support_req" model)

        # [Not using this approach] Delete the message request in the CSR dashboard
        # cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug).delete()
        # cust_support_req = CustomerSupportRequest.objects.get(room_slug=roomSlugParam)
        # print(f"Deleting the customer-support-request: {cust_support_req.room_slug} --- {cust_support_req.registered_user_email_normalized} --- {cust_support_req.assigned_cso}")
        # cust_support_req.delete()
        # # async_to_sync(cust_support_req.delete())



        #   --------------------     W O R K   H E R E     --------------------

        # it'll be similar to the following code-block
        # if not cust_support_req.is_dismissed:
        #     cust_support_req.is_dismissed = True
        #     cust_support_req.save()
        
        
        
        print('The conversation is marked as dismissed!')


        self.send(text_data=json.dumps({
            'conversation_is_dismissed': 'True',
            'common_cso_email': common_cso_email,
            'common_registered_user_email': common_registered_user_email,
            'roomSlugParam': roomSlugParam,
        }))

    # Human feedback post to frontend method
    def human_feedback(self, event):
        feedback = event['feedback']
        roomslug = event['roomslug']
        print(f'feedback (human_feedback): {feedback}')
        print(f'roomslug (human_feedback): {roomslug}')

        self.send(text_data=json.dumps({
            'feedback': True,
            'human_feedback': feedback,
            'roomslug': roomslug,
        }))

    # Multiline Reply Mode
    def multiline_reply_mode(self, event):
        mlr = event['mlr']
        roomslug = event['roomslug']
        print(f'multiline_reply (mlr): {mlr}')
        print(f'roomslug (mlr): {roomslug}')

        self.send(text_data=json.dumps({
            'MultilineReplyMode': True,     # Basically, it's important in the frontend socket currently
            'mlr': mlr,
            'roomslug': roomslug,
        }))
    
    # Send HF sending signal on MLR mode disabled
    def send_hf_on_mlr_disable(self, event):
        user_identity = event['user_identity']
        roomslug = event['roomslug']
        print(f'User identity (send_hf_on_mlr_disable): {user_identity}')
        print(f'roomslug (send_hf_on_mlr_disable): {roomslug}')

        self.send(text_data=json.dumps({
            'sendHfOnMlrDisable': True,
            'user_identity': user_identity,
            'roomslug': roomslug,
        }))
    
    # Conversational Reply Mode
    def conversational_reply_mode(self, event):
        cr = event['cr']
        roomslug = event['roomslug']
        print(f'conversational_reply (cr): {cr}')
        print(f'roomslug (cr): {roomslug}')

        self.send(text_data=json.dumps({
            'ConversationalReplyMode': True,     # Basically, it's important in the frontend socket currently
            'cr': cr,
            'roomslug': roomslug,
        }))
    
    # Send HF sending signal on CR mode disabled
    def send_hf_on_cr_disable(self, event):
        user_identity = event['user_identity']
        roomslug = event['roomslug']
        print(f'User identity (send_hf_on_cr_disable): {user_identity}')
        print(f'roomslug (send_hf_on_cr_disable): {roomslug}')

        self.send(text_data=json.dumps({
            'sendHfOnCrDisable': True,
            'user_identity': user_identity,
            'roomslug': roomslug,
        }))

    # Query Reply Mode
    def query_reply_mode(self, event):
        hifq = event['hifq']
        roomslug = event['roomslug']
        print(f'Query-reply mode (qrm): {hifq}')
        print(f'roomslug (qrm): {roomslug}')

        self.send(text_data=json.dumps({
            'QueryReplyMode': True,
            'hifq': hifq,
            'roomslug': roomslug,
        }))

    # Default method of "WebsocketConsumer" class
    def disconnect(self, *args, **kwargs):
        print("#"*50)
        if self.user_obj.id is not None:
            print('(CSO is about to disconnect!) Make query in the "ChatSupportUserOnline" model using cso-email, if found make the user offline!')
            # call the deactive_user_online() func
            async_to_sync(deactive_user_online(cso_email=self.user_obj.email, room_slug=self.room_name, channel_name=self.channel_name))
            
            # [NB]: This block is meant to sent signal-msg to the frontend-websocket (mainly to other users' that the user is offline now)
            # total_active_channel = count_active_channel(room_slug=self.room_name, cso_email=self.user_obj.email)
            # if len(total_active_channel) != 0:
            #     print(f"user has still active channels: {total_active_channel}, cannot make the user offline")
        
        if self.visitor_session_uuid is not None:
            print('(Visitor is about to disconnect!) Make query in the "ChatSupportUserOnline" model using visitor_session_uuid, if found make the user offline!')
            # call the deactive_user_online() func
            async_to_sync(deactive_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name, channel_name=self.channel_name))
            
            # [NB]: This block is meant to sent signal-msg to the frontend-websocket (mainly to other users' that the user is offline now)
            # total_active_channel = count_active_channel(room_slug=self.room_name, cso_email=self.user_obj.email)
            # if len(total_active_channel) != 0:
            #     print(f"user has still active channels: {total_active_channel}, cannot make the user offline")

        # TODO: Firstly, check if the total channel-connection of that individual user == 0 before discarding user-channel from the channel-group,
        #  so other users will also not be informed if that individual user "refreshes his/her screen" or "open duplicate tabs of the same chat-page"
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: CSOVisitorChatSuppportConsumer")
        print("#"*50)
