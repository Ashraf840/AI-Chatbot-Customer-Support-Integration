from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from ..models import User, User_Profile, User_signin_token_tms
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import UserPasswordResetForm
from django.contrib.auth.hashers import make_password
from django.urls.base import reverse
import json, requests


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


def updateCSOPasswordTMS(user, username, auth_password, set_password):
    """
    This method will user the chage-password-api to change the password of the user by his/her ownself
    """
    url = "https://tms-test.celloscope.net/api/v1/user/signin"
    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "user_id": f"{username}",
        "password": f"{auth_password}"
    })
    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    user_token=TMS_res_dict['token']['access_token']
    print("TMS_res_dict:", TMS_res_dict)

    # Store user-signin-token into the TMS
    try:
        User_signin_token_tms.objects.get(
            user_email=f"{user.email}",
            user_id=f"{user.username}",    
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

    # Reset/change the password of the user by his/her own credentials
    url = "https://tms-test.celloscope.net/api/v1/change-password"

    payload = json.dumps({
        "oldPassword": f"{auth_password}",
        "newPassword": f"{set_password}",
        "confirmPassword": f"{set_password}",
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json',
        'Referer': 'https://tms-test.celloscope.net/issuer',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    print("After changing CSO's password into TMS:", TMS_res_dict)
    return TMS_res_dict



# class PasswordResetView(LoginRequiredMixin, View):
class PasswordResetView(View):
    """
    User will be prompt to reset the pre-defined password at the first time login.
    """
    # TODO: make sure the user is authenticated firstly, otherwise redirect to landing page
    # TODO: make user.is_first_login=True in the post method's successful code-block
    # login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    template_name = 'authenticationApp/password_reset.html'
    form_class = UserPasswordResetForm
    context={
        'title': 'Password Reset', 
    }
    
    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form_class()
        # TODO: check if the "user.is_first_login" field is "True", otherwise redirect to landing page. 
        # Apply this TODO in both get & post method of this class.
        email = kwargs['email']     # [Ref]: https://ordinarycoders.com/blog/article/django-class-based-views
        # print('email (sent from URL - get method):', email)
        user = get_object_or_404(User, email=email)     # [Ref]: https://stackoverflow.com/a/65598612
        # print('User object (Password Reset class):', user)
        if user.is_first_login:
            print("[PasswordResetView() Class-get-method] User logged in for the first time!")
            # self.context['form'] = self.form_class()
            return render(request, self.template_name, context=self.context)
        else:
            return redirect('homeApplication:LangingPage')

    def post(self, request, *args, **kwargs):
        self.context['form'] = self.form_class(request.POST)
        form = self.context['form']
        email = kwargs['email']
        print('email (sent from URL - post method):', email)
        user = get_object_or_404(User, email=email)
        if user.is_first_login:
            print("[PasswordResetView() Class-post-method] About to change the user password, User will no longer be a first-time-login-er!")
            # TODO: Change user password here, after checking if password1 == password2, otherwise redirect to login page
            # TODO: Change the user.is_first_login = False
            if form.is_valid():
                password1 = form.cleaned_data['password']
                password2 = form.cleaned_data['repeat_password']
                # print('password1:', password1)
                # print('password2:', password2)
                if password1 == password2:
                    user.is_first_login = False
                    hashed_pass = make_password(password1)
                    user.password = hashed_pass    # hashed before setting new password
                    user.save()
                    # TODO: Later, redirect the users to their dashboard according to their user role
                    # [NB]: Didn't understand why the user is redirected to login again at this stage.
                    print("[PasswordResetView() Class-post-method] password is set successfully!")

                    # TODO: UPDATE CSO's PASSWORD REGARDING RESET-PASSWORD-API
                    updateCSOPasswordTMS(user=user, username=user.username, auth_password=user.initial_password, set_password=password1)




                    return redirect('staffApplication:CsoWorkload:CsoDashboard')
                else:
                    print("[PasswordResetView() Class-post-method] password didn't matched!")
                    return redirect(reverse(
                        'authenticationApplication:PasswordResetView', 
                        kwargs={"email": user.email}
                    ))
            # TODO: Later, redirect the users to their login-page according to their user role
            print('[PasswordResetView() Class-post-method] form is not valid!')
            return redirect(reverse(
                'authenticationApplication:PasswordResetView', 
                kwargs={"email": user.email}
            ))
        else:
            return redirect('homeApplication:LangingPage')