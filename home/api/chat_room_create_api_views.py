from rest_framework.views import APIView
# from ..models import UserChatbotSocket
# from authenticationApp.models import User, User_Profile
# from django.http import Http404
from rest_framework.response import Response
# from rest_framework import status
# from django.http import HttpResponse, JsonResponse
# from .user_detail_serializer import UserSerializer, UserProfileSerailizer
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

            user_organization = request.data['user_organization']
            location = request.data['location']
            district = request.data['district']
            division = request.data['division']
            # print(f"user_organization: {user_organization} --- location: {location} --- district: {district} --- division: {division}")

            chatbot_socket_id = request.data['chatbot_socket_id']
            issuerOid = request.data['issuerOid']
            print("TMS Issuer Oid:", issuerOid)
            user_chatbot_socket = UserChatbotSocket.objects.filter(chatbot_socket_id=chatbot_socket_id)
            if len(user_chatbot_socket) == 1:
                print(user_chatbot_socket)
                # Check the message-distribution-threshholds first
                active_cso = CSOOnline.get_active_cso(
                    user_organization=user_organization,
                    location=location,
                    district=district,
                    division=division
                )
                if len(active_cso) == 0:
                    return Response("No CSO is currently available!")
                if len(active_cso) == 1:
                    # print(f'Active cso: {active_cso[0]["cso_email"]}')
                    total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=active_cso[0]["cso_email"])
                    if len(total_msg) >= 5:
                        return Response("No CSO is currently available!")
                    else:
                        # return JsonResponse({
                        #     'msg': 'Single CSO is avaiable!',
                        #     'cso_email': active_cso
                        # })
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
                    print("len(active_cso) > 1")
                    total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso()
                    msg_req = []
                    print("total_msg:", total_msg)
                    print("total_msg length:", len(total_msg))
                    # print("msg_req length:", len(msg_req))
                    if len(msg_req) == 0:
                        print("len(msg_req) == 0")
                        # active_cso_emails = [ac['cso_email'] for ac in active_cso]
                        # selected_active_cso_email = random.choice(active_cso_emails)
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
                    if len(msg_req) > 0:
                        print("len(msg_req) > 0")
                        for msg in total_msg:
                            msg_req.append(msg['assigned_cso'])
                        msg_req_set = set(msg_req)
                        msg_count = []
                        msg_req_list = list(msg_req_set)
                        for i in msg_req_list:
                            msg_count.append(msg_req.count(i))
                        msg_req_list = msg_req_list
                        print("msg_req_list:", msg_req_list)
                        for x in msg_count:
                            if x < 5:   # if there is any cso whose handling less than 5 chats at the current moment
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
                            return Response("No CSO is currently available!")


                # print("sent an information to the socket consumer!")
                # channel_layer = get_channel_layer()
                # email_normalized="".join(ch for ch in user_email if ch.isalnum())
                # async_to_sync(channel_layer.group_send)(
                #     f'user_chatbot_socket_{email_normalized}',
                #     {
                #         'type': 'auto_create_chatroom', 
                #         'user_email': user_chatbot_socket[0].user_email,
                #         'chatbot_socket_id': user_chatbot_socket[0].chatbot_socket_id,
                #     }
                # )
                pass
            print("Hitting the 'ChatRoomCreateAPISocket()' class API")
            return Response("Hitting the 'ChatRoomCreateAPISocket()' class API")
        return Response("Please send valid 'user_email' & 'chatbot_socket_id' in a JSON format.")

