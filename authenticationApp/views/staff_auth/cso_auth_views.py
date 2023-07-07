from django.shortcuts import render, redirect
from django.views.generic import View
from ...forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
import requests, json
from ...models import User_signin_token_tms
from django.contrib import messages


def TMSLogin(username, password):
    url = "https://tms-test.celloscope.net/api/v1/user/signin"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        # "user_id": "chat.bot",
        "user_id": f"{username}",
        "password": f"{password}"
    })
    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    return TMS_res_dict


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
        'title': 'Help Desk Login', 
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
            
            
            # if user is not None and TMS_res_dict['status']:
            if user is not None:
                # TODO: Check if the user has the perm of "is_cso", if user is "is_user", then redirect to the user login page including an error-msg, otherwise throw an error-msg only.
                if user.is_user:
                    msg = 'Login using the user login system!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:UserAuth:UserLoginPageView')
                elif user.is_cso:
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
                    
                    print("This CSO is not loggin in for the first time!")
                    # TODO: Try to fetch signin-token from TMS
                    tmsLoginData = TMSLogin(username=user.username, password=form.cleaned_data['password'])
                    if tmsLoginData['status']:
                        print(tmsLoginData)
                        print(tmsLoginData['status'])
                        print(tmsLoginData['token']['access_token'])
                        print(tmsLoginData['token']['token_type'])

                        # TODO: store user-signin-token to db-table ("User Signin Token (TMS)"). Firstly, check if there is any access-token record already in the db for removing that before creating a new-record
                        # TODO: CODE OPTIMIZATION IN USER-ACCESS-TOKEN-CREATION
                        try:
                            User_signin_token_tms.objects.get(
                                user_email=user.email,
                                user_id=user.username,    
                            ).delete()
                            user_token_creation(user_email=user.email,
                                user_id=user.username,
                                user_token=tmsLoginData['token']['access_token'],
                                token_type=tmsLoginData['token']['token_type'])
                        except User_signin_token_tms.DoesNotExist:
                            user_token_creation(user_email=user.email,
                                user_id=user.username,
                                user_token=tmsLoginData['token']['access_token'],
                                token_type=tmsLoginData['token']['token_type'])

                    login(request, user)
                    # TODO: Get TMS-signin-token & store into DB table (User Signin Token)
                    return redirect('staffApplication:CsoWorkload:CsoDashboard')
                else:
                    msg = 'Permission denied!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:CsoAuth:CSOLoginPageView')
            # CSO login unsuccessful
            msg = 'Invalid credentials!'
            messages.info(request, '%s' % msg)
            return redirect('authenticationApplication:CsoAuth:CSOLoginPageView')
        self.context['message'] = 'Login failed!'
        return render(request, self.template_name, context=self.context)


# TODO: [Done] Create CSO logout functionality inside "authenticationApp\urls\staff_auth\cso_auth_urls.py"