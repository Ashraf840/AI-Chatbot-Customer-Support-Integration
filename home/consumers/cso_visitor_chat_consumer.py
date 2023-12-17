from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import CSOVisitorMessage, CustomerSupportRequest, CSOVisitorConvoInfo, RemarkResolution
from ..user_connectivity_models import ChatSupportUserOnline, ChatSupportUserConnectedChannels


def create_channel_conn(room_slug, channel_name, cso_email=None, visitor_session_uuid=None):
    print('*'*10, "create_channel_conn() func is called")
    print("room slug:", room_slug)
    channel_name = channel_name.replace('specific.', '')
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
    channel_name = channel_name.replace('specific.', '')
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
    

def make_user_online(user):
    if not user.is_active:
        user.is_active = True
        user.save()

def make_user_offline(user):
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
            make_user_online(user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
        except ChatSupportUserOnline.DoesNotExist:
            user_online_obj = ChatSupportUserOnline.objects.create(cso_email=cso_email, room_slug=room_slug)
            print('Created a active cso user record!', user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('check visitor-user online using session-uuid in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Found active visitor user record!', user_online_obj)
            make_user_online(user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)
        except ChatSupportUserOnline.DoesNotExist:
            user_online_obj = ChatSupportUserOnline.objects.create(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Created a active visitor user record!', user_online_obj)
            create_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)


def count_active_channel(room_slug, cso_email=None, visitor_session_uuid=None):
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
            remove_channel_conn(room_slug=room_slug, channel_name=channel_name, cso_email=cso_email)
            total_active_channel = count_active_channel(room_slug=room_slug, cso_email=cso_email)
            print('total_active_channel (cso):', total_active_channel)
            if len(total_active_channel) == 0:
                make_user_offline(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            print('User doesn\'t exist to make the user offline!')
    
    if visitor_session_uuid is not None:
        print("visitor session uuid:", visitor_session_uuid)
        print('check visitor-user online using session-uuid in the "ChatSupportUserOnline" model.')
        try:
            user_online_obj = ChatSupportUserOnline.objects.get(visitor_session_uuid=visitor_session_uuid, room_slug=room_slug)
            print('Intially make the user (visitor) offline!', user_online_obj)
            remove_channel_conn(room_slug=room_slug, channel_name=channel_name, visitor_session_uuid=visitor_session_uuid)
            total_active_channel = count_active_channel(room_slug=room_slug, visitor_session_uuid=visitor_session_uuid)
            print('total_active_channel (visitor):', total_active_channel)
            if len(total_active_channel) == 0:
                make_user_offline(user_online_obj)
        except ChatSupportUserOnline.DoesNotExist:
            print('User (visitor) doesn\'t exist to make the user offline!')


def save_message(message, user_identity, room_slug):
    msg = CSOVisitorMessage.objects.create(
        message=message,
        user_identity=user_identity, 
        room_slug=room_slug
    )
    return msg


class CSOVisitorChatSuppportConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super(CSOVisitorChatSuppportConsumer, self).__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.is_visitor_intruder = False
        self.user_obj = None
        self.visitor_session_uuid = None
    
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: CSOVisitorChatSuppportConsumer")
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_obj = self.scope['user']
        print(f'Channel name: {self.channel_name}')

        if self.user_obj.id is not None:
            print('Check if the cso-user exists in the "ChatSupportUserOnline" table; if not found, then create a record in that table & later create channel record of the cso-user! (both "ChatSupportUserOnline" & "ChatSupportUserConnectedChannels" tables use cso-email)')
            async_to_sync(active_user_online(cso_email=self.user_obj.email, room_slug=self.room_name, channel_name=self.channel_name))
        else:
            visitor_support_req = CustomerSupportRequest.objects.filter(
                room_slug=self.room_name,
            ).order_by('-created_at')
            if visitor_support_req:
                self.visitor_session_uuid = visitor_support_req[0].visitor_session_uuid
                print('visitor session uuid:', self.visitor_session_uuid)
                print('check if there is any record with the "visitor_session_uuid", if not found any then create a record in "ChatSupportUserOnline" table & later create channel of the visitor-user! (both "ChatSupportUserOnline" & "ChatSupportUserConnectedChannels" tables use visitor-session-uuid)')
                async_to_sync(active_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name, channel_name=self.channel_name))
            else:
                self.is_visitor_intruder = True



        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.accept())
        print("#"*50)

    def receive(self, text_data=None, bytes_data=None):
        if not self.is_visitor_intruder:
            print("#"*50)
            data = json.loads(text_data)

            if 'message' in data:
                message = data['message']
                user_identity = data['user_identity']
                roomslug = data['roomslug']

                msg = async_to_sync(save_message(
                    message=message,
                    user_identity=user_identity,
                    room_slug=roomslug
                ))
                print(f"Saved msg: {msg.awaitable.created_at}")

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user_identity': user_identity,
                        'roomslug': roomslug,
                    }
                )

            if 'cso_user_convo_cancelled' in data:
                cso_email = data['cso_email']
                reg_user_email = data['reg_user_email']
                room_slug = data['roomslug']
                print('The conversation is cancelled by the user!')
                print("User email:", reg_user_email)
                print("CSO email:", cso_email)

                cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=room_slug)
                cso_visitor_convo_info.is_cancelled, cso_visitor_convo_info.is_connected = True, False
                cso_visitor_convo_info.save()

                cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug).delete()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_convo_cancelled',
                        'cso_email': cso_email,
                        'reg_user_email': reg_user_email,
                        'room_slug': room_slug,
                    }
                )

            if 'feedback' in data:
                feedback = data['feedback']
                fc_uid = data['fc_uid']
                roomslug = data['roomslug']
                # print("Feedback container uid (backend):", fc_uid)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'human_feedback',
                        'feedback': feedback,
                        'fc_uid': fc_uid,
                        'roomslug': roomslug,
                    }
                )
            
            if 'mlr' in data:
                mlr = data['mlr']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'multiline_reply_mode',
                        'mlr': mlr,
                        'roomslug': roomslug,
                    }
                )
            
            if 'sendHfOnMlrDisable' in data and data['sendHfOnMlrDisable']=='Send HF on MLR mode disble':
                print("Sent socket signal to chatroom to send HF to customer end; since HDO has disabled the MLR mode!")
                user_identity = data['user_identity']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_hf_on_mlr_disable',
                        'user_identity': user_identity,
                        'roomslug': roomslug,
                    }
                )
            
            if 'cr' in data:
                cr = data['cr']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'conversational_reply_mode',
                        'cr': cr,
                        'roomslug': roomslug,
                    }
                )
            
            if 'sendHfOnCrDisable' in data and data['sendHfOnCrDisable']=='Send HF on CR mode disble':
                print("Sent socket signal to chatroom to send HF to customer end; since HDO has disabled the CR mode!")
                user_identity = data['user_identity']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_hf_on_cr_disable',
                        'user_identity': user_identity,
                        'roomslug': roomslug,
                    }
                )

            if 'hifq' in data:
                hifq = data['hifq']
                roomslug = data['roomslug']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'query_reply_mode',
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
            self.disconnect(self)
    
    def chat_message(self, event):
        message = event['message']
        user_identity = event['user_identity']
        roomslug = event['roomslug']
        self.send(text_data=json.dumps({
            'message': message,
            'user_identity': user_identity,
            'roomslug': roomslug,
        }))


    def support_resolved(self, event):
        cso_email = event['cso_email']
        reg_user_email = event['reg_user_email']
        ticket_issue_oid = event['ticket_issue_oid']
        user_signing_token_tms = event['user_signing_token_tms']
        remark_input_resolve_value = event['remark_input_resolve_value']
        roomSlugParam = event['roomSlugParam']
        print('\n', '-'*50)
        print('The support is resolved')
        print("ticket_issue_oid:", ticket_issue_oid)
        print("user_signing_token_tms:", user_signing_token_tms)
        print("remark_input_resolve_value:", remark_input_resolve_value)
        print("cso_email:", cso_email)
        print("reg_user_email:", reg_user_email)
        print("roomSlugParam:", roomSlugParam)
        print('\n', '-'*50)

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
        remark_input_dismiss_value = event['remark_input_dismiss_value']
        roomSlugParam = event['roomSlugParam']

        print('\n', '-'*50)
        print('The chat conversation is dismissed by the user!')
        print("common_cso_email:", common_cso_email)
        print("common_registered_user_email:", common_registered_user_email)
        print("remark_input_dismiss_value:", remark_input_dismiss_value)
        print("roomSlugParam:", roomSlugParam)
        print('\n', '-'*50)
        print('The conversation is marked as dismissed!')


        self.send(text_data=json.dumps({
            'conversation_is_dismissed': 'True',
            'common_cso_email': common_cso_email,
            'common_registered_user_email': common_registered_user_email,
            'roomSlugParam': roomSlugParam,
        }))

    def human_feedback(self, event):
        feedback = event['feedback']
        fc_uid = event['fc_uid']
        roomslug = event['roomslug']
        print(f'feedback (human_feedback): {feedback}')
        print(f'roomslug (human_feedback): {roomslug}')

        self.send(text_data=json.dumps({
            'feedback': True,
            'human_feedback': feedback,
            'fc_uid': fc_uid,
            'roomslug': roomslug,
        }))

    # Multiline Reply Mode
    def multiline_reply_mode(self, event):
        mlr = event['mlr']
        roomslug = event['roomslug']
        print(f'multiline_reply (mlr): {mlr}')
        print(f'roomslug (mlr): {roomslug}')

        self.send(text_data=json.dumps({
            'MultilineReplyMode': True,
            'mlr': mlr,
            'roomslug': roomslug,
        }))
    
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
    
    def conversational_reply_mode(self, event):
        cr = event['cr']
        roomslug = event['roomslug']
        print(f'conversational_reply (cr): {cr}')
        print(f'roomslug (cr): {roomslug}')

        self.send(text_data=json.dumps({
            'ConversationalReplyMode': True,
            'cr': cr,
            'roomslug': roomslug,
        }))
    
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

    def disconnect(self, *args, **kwargs):
        print("#"*50)
        if self.user_obj.id is not None:
            print('(CSO is about to disconnect!) Make query in the "ChatSupportUserOnline" model using cso-email, if found make the user offline!')
            async_to_sync(deactive_user_online(cso_email=self.user_obj.email, room_slug=self.room_name, channel_name=self.channel_name))
        
        if self.visitor_session_uuid is not None:
            print('(Visitor is about to disconnect!) Make query in the "ChatSupportUserOnline" model using visitor_session_uuid, if found make the user offline!')
            async_to_sync(deactive_user_online(visitor_session_uuid=self.visitor_session_uuid, room_slug=self.room_name, channel_name=self.channel_name))

        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: CSOVisitorChatSuppportConsumer")
        print("#"*50)
