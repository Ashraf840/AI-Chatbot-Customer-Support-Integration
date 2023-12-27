from .user_serializer import UserSerializer, UserProfileSerailizer
from rest_framework.views import APIView
from ..models import User, User_Profile
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


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
