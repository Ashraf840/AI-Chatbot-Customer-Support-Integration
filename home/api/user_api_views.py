from rest_framework.views import APIView
from ..models import UserChatbotSocket
from authenticationApp.models import User, User_Profile
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from .user_detail_serializer import UserSerializer, UserProfileSerailizer, UserChatbotSocketSerializer


class UserDetailAPIChatbotSocket(APIView):
    """
    Retrieve User Detail (based on chatbot's socket id)
    """
    def get_user_object(self, email):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
        
    def get_userChatbotSocket_object(self, chatbotSocketID):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return UserChatbotSocket.objects.get(chatbot_socket_id=chatbotSocketID)
        except UserChatbotSocket.DoesNotExist:
            raise Http404
    
    def get_user_profile_object(self, email):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return User_Profile.objects.get(user_email=email)
        except User_Profile.DoesNotExist:
            raise Http404
    
    def Merge(self, user_instance, user_profile_instance, userChatbotSocket_instance):
        res = {**user_instance, **user_profile_instance, **userChatbotSocket_instance}
        return res

    def get(self, request, chatbotSocketID, format=None):
        userChatbotSocket = self.get_userChatbotSocket_object(chatbotSocketID=chatbotSocketID)
        userChatbotSocket_serializer = UserChatbotSocketSerializer(userChatbotSocket)
        user_email = userChatbotSocket.user_email
        user_instance = self.get_user_object(email=user_email)
        user_serializer = UserSerializer(user_instance)
        user_profile_instance = self.get_user_profile_object(email=user_email)
        user_profile_serializer = UserProfileSerailizer(user_profile_instance)
        print("user_profile_serializer: ", dict(user_profile_serializer.data))
        user_userProfile_combined = self.Merge(dict(user_serializer.data), dict(user_profile_serializer.data), dict(userChatbotSocket_serializer.data))

        return Response(user_userProfile_combined)

    def post(self, request, format=None):
        # result = request
        if 'chatbot_socket_id' in request.data:
            print("chatbot socket id:", request.data['chatbot_socket_id'])
            userChatbotSocket = self.get_userChatbotSocket_object(chatbotSocketID=request.data['chatbot_socket_id'])
            userChatbotSocket_serializer = UserChatbotSocketSerializer(userChatbotSocket)
            # print(dict(userChatbotSocket_serializer.data))
            user_email = userChatbotSocket.user_email
            user_instance = self.get_user_object(email=user_email)
            user_serializer = UserSerializer(user_instance)
            user_profile_instance = self.get_user_profile_object(email=user_email)
            user_profile_serializer = UserProfileSerailizer(user_profile_instance)
            # print(dict(user_profile_serializer.data))
            user_userProfile_combined = self.Merge(dict(user_serializer.data), dict(user_profile_serializer.data), dict(userChatbotSocket_serializer.data))

            return Response(user_userProfile_combined)
        return Response("Please send 'chatbot_socket_id' in a JSON format.")
    
        # NB: THE FOLLOWING RESPONSES COULDN'T RETURN THE BANGLA NAME OF THE USER
        # return JsonResponse(user_userProfile_combined)
        return JsonResponse({
            'User': user_serializer.data,
            'User_Profile': user_profile_serializer.data
        })
        return Response(user_serializer.data)
