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
        "user_id": f"{username}",
        "password": f"{password}"
    })
    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    return TMS_res_dict


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
            
            
            if user is not None:
                if user.is_user:
                    msg = 'Login using the user login system!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:UserAuth:UserLoginPageView')
                elif user.is_cso:
                    if user.is_first_login:
                        print("[CSOLoginPageView() Class-post-method] User logged in for the first time!")
                        return redirect(reverse(
                            'authenticationApplication:PasswordResetView', 
                            kwargs={"email": user.email}
                        ))
                    
                    print("This CSO is not loggin in for the first time!")
                    tmsLoginData = TMSLogin(username=user.username, password=form.cleaned_data['password'])
                    if tmsLoginData['status']:
                        print(tmsLoginData)
                        print(tmsLoginData['status'])
                        print(tmsLoginData['token']['access_token'])
                        print(tmsLoginData['token']['token_type'])

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
                    return redirect('staffApplication:CsoWorkload:CsoDashboard')
                else:
                    msg = 'Permission denied!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:CsoAuth:CSOLoginPageView')
            msg = 'Invalid credentials!'
            messages.info(request, '%s' % msg)
            return redirect('authenticationApplication:CsoAuth:CSOLoginPageView')
        self.context['message'] = 'Login failed!'
        return render(request, self.template_name, context=self.context)
