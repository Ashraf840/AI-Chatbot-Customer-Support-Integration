from .user_serializer import UserSerializer, UserProfileSerailizer
from rest_framework.views import APIView
from ..models import User, User_Profile
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from home.models import UserChatbotSocket
import random


class UserAuthAPI(APIView):
    def post(self, request):
        senderId = request.data["senderId"]
        socket_id = UserChatbotSocket.objects.filter(chatbot_socket_id=senderId)
        is_authenticated = False
        if len(socket_id) > 0:
            is_authenticated = True
            print("User is authenticated!")
        else:
            print("User is not authenticated!")
        print("senderId:", senderId)
        data = {'is_authenticated': is_authenticated}
        return Response(data)


class UserLoginRegAutomationAPI(APIView):
    def post(self, request):
        print("UserLoginRegAutomationAPI - request.data:", request.data)
        nid = request.data.get('nid_num', None)
        phone = request.data.get('phone', None)
        district = request.data.get('district_name', None)
        user_query = request.data.get('user_query', None)
        user_login = request.data.get('user_login', None)
        user_registration = request.data.get('user_registration', None)
        existing_user_password = request.data.get('existing_user_password', None)
        # print("UserLoginRegAutomationAPI - user_login:", user_login)

        if user_login:
            # If password is provided from the login workflow from the chatbot-login.js file, then use this block
            if existing_user_password:
                print("User password is provided. Cross check with the automatically provided email from the frontend. if password is matched, then send the user-email & password to the frontend again. Thus it will populate a login-form with the value & automatically submit that in the user-login view! Include **kwargs so that further the system can generate the prompt to connect to HDO, if pressed YES, then hit the chat romm create api from there.")
            
            # Check if there is any user containing the phone number
            user = User.objects.filter(phone=phone)
            # import pdb; pdb.set_trace()
            if len(user) > 0:
                print("User account exists! Add user-email automatically from here to another method of this class.")
                # print("user email:", user[0].email)
                return Response({
                    'result': 'User account exists',
                    # 'email': user[0].email,
                    'phone': phone,
                }, status=status.HTTP_200_OK)     # Ask for password from the user, sent the user email to the frontend also
            else:
                print("User account doesn't exist")
                return Response({'result': 'User account doesn\'t exist'})
        
        if user_registration:
            print("Make user registration & automatically login the user to the system!")
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            # Generate random username
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            length = 12
            username = ''.join(random.choice(chars) for i in range(length))
            # Create user account
            user = User(
                email=email,
                username=username,
                phone=phone,
            )
            user.is_user = True
            user.set_password(password)
            user.save()
            # Create user profile
            user_profile = User_Profile.objects.get(user_email=user.email)
            user_profile.district = district
            user_profile.user_NID_no = nid
            user_profile.save()
            return Response({
                'result': 'User account is created & logged in!',
                'email': user.email,
                'password': password
            })


class UserDetailAPI(APIView):
    """
    Retrieve User Detail
    """
    def get_user_object(self, email):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
    
    def get_user_profile_object(self, email):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return User_Profile.objects.get(user_email=email)
        except User_Profile.DoesNotExist:
            raise Http404
    
    def Merge(self, user_instance, user_profile_instance):
        res = {**user_instance, **user_profile_instance}
        return res

    def get(self, request, email, format=None):
        user_instance = self.get_user_object(email=email)
        user_serializer = UserSerializer(user_instance)
        user_profile_instance = self.get_user_profile_object(email=email)
        user_profile_serializer = UserProfileSerailizer(user_profile_instance)
        print(dict(user_profile_serializer.data))
        user_userProfile_combined = self.Merge(dict(user_serializer.data), dict(user_profile_serializer.data))

        return Response(user_userProfile_combined)
    
        # NB: THE FOLLOWING RESPONSES COULDN'T RETURN THE BANGLA NAME OF THE USER
        # return JsonResponse(user_userProfile_combined)
        return JsonResponse({
            'User': user_serializer.data,
            'User_Profile': user_profile_serializer.data
        })
        return Response(user_serializer.data)
