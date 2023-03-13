from django.shortcuts import render, redirect
from django.views.generic import View
from ...forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
import requests, json
from ...models import User_signin_token_tms


# User token creation method
def user_token_creation(user_email=None,
                        user_id=None,
                        user_token=None,
                        token_type=None):
    User_signin_token_tms.objects.create(
        user_email=user_email,
        user_id=user_id,
        user_token=user_token,
        token_type=token_type
    )


# Concept Ref: https://openclassrooms.com/en/courses/7107341-intermediate-django/7263527-create-a-login-page-with-class-based-views
class CSOLoginPageView(View):
    template_name = 'authenticationApp/cso_login.html'
    form_class = UserLoginForm
    context={
        'title': 'CSO Login', 
    }
    
    def get(self, request):
        self.context['form'] = self.form_class()
        return render(request, self.template_name, context=self.context)
        
    def post(self, request):
        self.context['form'] = self.form_class(request.POST)
        form = self.context['form']
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            # TODO: Try to fetch signin-token from TMS
            url = "https://tms-test.celloscope.net/api/v1/user/signin"
            headers = {
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                # "user_id": "chat.bot",
                "user_id": f"{user.username}",
                "password": f"{form.cleaned_data['password']}"
            })
            TMS_res = requests.post(url, headers=headers, data=payload)
            TMS_res_dict = TMS_res.json()
            print(TMS_res_dict)
            print(TMS_res_dict['status'])
            print(TMS_res_dict['token']['access_token'])
            print(TMS_res_dict['token']['token_type'])
            if user is not None and TMS_res_dict['status']:
                # TODO: store user-signin-token to db-table ("User Signin Token (TMS)"). Firstly, check if there is any access-token record already in the db for removing that before creating a new-record
                # TODO: CODE OPTIMIZATION IN USER-ACCESS-TOKEN-CREATION
                try:
                    User_signin_token_tms.objects.get(
                        user_email=user.email,
                        user_id=user.username,    
                    ).delete()
                    user_token_creation(user_email=user.email,
                        user_id=user.username,
                        user_token=TMS_res_dict['token']['access_token'],
                        token_type=TMS_res_dict['token']['token_type'])
                except User_signin_token_tms.DoesNotExist:
                    user_token_creation(user_email=user.email,
                        user_id=user.username,
                        user_token=TMS_res_dict['token']['access_token'],
                        token_type=TMS_res_dict['token']['token_type'])
                    
                
                
                # TODO: Only CSO will be able to access the CSO-dashboard; restrict & redirect User with "is_user" permission to user login panel
                # TODO: Check if the user login is the first time
                if user.is_first_login:
                    print("[CSOLoginPageView() Class-post-method] User logged in for the first time!")
                    # TODO: Redirect the user to password-reset view after logging in
                    # login(request, user)  # NB:[Optional]: User has to login again after resetting password
                    return redirect(reverse(
                        'authenticationApplication:PasswordResetView', 
                        kwargs={"email": user.email}
                    ))
                login(request, user)
                # TODO: Get TMS-signin-token & store into DB table (User Signin Token)
                return redirect('staffApplication:CsoWorkload:CsoDashboard')
        self.context['message'] = 'Login failed!'
        return render(request, self.template_name, context=self.context)


# TODO: [Done] Create CSO logout functionality inside "authenticationApp\urls\staff_auth\cso_auth_urls.py"