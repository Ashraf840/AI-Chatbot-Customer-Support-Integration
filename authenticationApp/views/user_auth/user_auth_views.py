from django.shortcuts import render, redirect
from django.views.generic import View
from ...forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.urls.base import reverse


# Concept Ref: https://openclassrooms.com/en/courses/7107341-intermediate-django/7263527-create-a-login-page-with-class-based-views
class UserLoginPageView(View):
    template_name = 'authenticationApp/user_login.html'
    form_class = UserLoginForm
    context={
        'title': 'User Login', 
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
                # TODO: Check if the user login is the first time
                # if user.is_first_login:
                #     print("[CSOLoginPageView() Class-post-method] User logged in for the first time!")
                #     # TODO: Redirect the user to password-reset view after logging in
                #     # login(request, user)  # NB:[Optional]: User has to login again after resetting password
                #     return redirect(reverse(
                #         'authenticationApplication:PasswordResetView', 
                #         kwargs={"email": user.email}
                #     ))
                login(request, user)
                return redirect('homeApplication:LangingPage')
                # return redirect('staffApplication:CsoWorkload:CsoDashboard')
        self.context['message'] = 'Login failed!'
        return render(request, self.template_name, context=self.context)


# TODO: [Done] Create CSO logout functionality inside "authenticationApp\urls\staff_auth\cso_auth_urls.py"