from django.shortcuts import render, redirect
from django.views.generic import View
from ...forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from django.contrib import messages


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
                if user.is_user:
                    login(request, user)
                    return redirect('homeApplication:LangingPage')
                elif user.is_cso:
                    msg = 'Login using the HDO login system!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:CsoAuth:CSOLoginPageView')
                else:
                    msg = 'Permission denied!'
                    messages.info(request, '%s' % msg)
                    return redirect('authenticationApplication:UserAuth:UserLoginPageView')
            msg = 'Invalid credentials!'
            messages.info(request, '%s' % msg)
            return redirect('authenticationApplication:UserAuth:UserLoginPageView')
        self.context['message'] = 'Login failed!'
        return render(request, self.template_name, context=self.context)
