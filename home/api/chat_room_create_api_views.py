from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import UserChatbotSocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from staffApp.cso_connectivity_models import CSOOnline
from home.models import CustomerSupportRequest
import random
from django.http import HttpResponse, JsonResponse




class ChatRoomCreateAPISocket(APIView):
    """
    API to send information to channel "ChatbotUserChatConsumer" to trigger the supportReq() function in the frontend through channels-webSocket.
    """
    def post(self, request, format=None):
        if 'user_email' in request.data and 'chatbot_socket_id' in request.data:
            user_email = request.data['user_email']
            email_normalized="".join(ch for ch in user_email if ch.isalnum())

            user_organization = request.data['user_organization']
            location = request.data['location']
            district = request.data['district']
            division = request.data['division']

            chatbot_socket_id = request.data['chatbot_socket_id']
            issuerOid = request.data['issuerOid']
            user_chatbot_socket = UserChatbotSocket.objects.filter(chatbot_socket_id=chatbot_socket_id)

            channel_layer = get_channel_layer()

            try:
                if bool(request.data['prompt_user']):
                    print("prompt_user:", request.data['prompt_user'])
                    async_to_sync(channel_layer.group_send)(
                        f'user_chatbot_socket_{email_normalized}',
                        {
                            'type': 'prompt_chatroom_create',
                            'user_email': user_chatbot_socket[0].user_email,
                            'chatbot_socket_id': user_chatbot_socket[0].chatbot_socket_id,
                            'issuerOid': issuerOid,
                            'user_organization': user_organization,
                            'location': location,
                            'district': district,
                            'division': division,
                        }
                    )
            except KeyError as error:
                print("Create user chatroom! Called Class Method: ChatRoomCreateAPISocket()! No 'prompt_user' key.")
                
                user_chatbot_socket = UserChatbotSocket.objects.filter(chatbot_socket_id=chatbot_socket_id)

                if len(user_chatbot_socket) == 1:
                    active_cso = CSOOnline.get_active_cso(
                        user_organization=user_organization,
                        location=location,
                        district=district,
                        division=division,
                        loc_support_confirmation=True
                    )

                    if len(active_cso) == 0:
                        return Response("No CSO is currently available!")
                    if len(active_cso) == 1:
                        total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=active_cso[0]["cso_email"])
                        if len(total_msg) >= 5:
                            return Response("No CSO is currently available!")
                        else:
                            channel_layer = get_channel_layer()
                            email_normalized="".join(ch for ch in user_email if ch.isalnum())
                            async_to_sync(channel_layer.group_send)(
                                f'user_chatbot_socket_{email_normalized}',
                                {
                                    'type': 'auto_create_chatroom', 
                                    'user_email': user_chatbot_socket[0].user_email,
                                    'chatbot_socket_id': user_chatbot_socket[0].chatbot_socket_id,
                                    'issuerOid': issuerOid,
                                }
                            )
                    if len(active_cso) > 1:
                        channel_layer = get_channel_layer()
                        email_normalized="".join(ch for ch in user_email if ch.isalnum())
                        async_to_sync(channel_layer.group_send)(
                                f'user_chatbot_socket_{email_normalized}',
                                {
                                    'type': 'auto_create_chatroom',
                                    'user_email': user_chatbot_socket[0].user_email,
                                    'chatbot_socket_id': user_chatbot_socket[0].chatbot_socket_id,
                                    'issuerOid': issuerOid,
                                }
                            )
                        return Response("CSO is avaiable!")

                    print("Hitting the 'ChatRoomCreateAPISocket()' class API")

            return Response("Hitting the 'ChatRoomCreateAPISocket()' class API")
        return Response("Please send valid 'user_email' & 'chatbot_socket_id' in a JSON format.")

