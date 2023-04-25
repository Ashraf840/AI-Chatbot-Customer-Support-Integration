"""schoolManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from .custom_admin_panel import CustomAdminSite
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib.admin.forms import AdminAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# custom_admin_site = CustomAdminSite(name='ibas_admin')


# class CustomAdminLogin(View):
#     template_name = 'admin/login.html'
#     form_class = AdminAuthenticationForm
#     context={
#         'title': 'CSO Login', 
#     }

#     def get(self, request):
#         self.context['form'] = self.form_class()
#         print("CustomAdminLogin() class is called!")
#         return render(request, self.template_name, context=self.context)

#     def post(self, request):
#         self.context['form'] = self.form_class(request.POST)
#         form = self.context['form']
#         if form.is_valid():
#             user = authenticate(
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password'],
#             )
#             login(request, user)
#         self.context['message'] = 'Login failed!'
#         return redirect('adminURL')
#         return render(request, "admin/index.html", context=self.context)
#         return redirect(reverse(
#             'authenticationApplication:PasswordResetView', 
#             kwargs={"email": user.email}
#         ))



urlpatterns = [
    # path('admin/login/', CustomAdminLogin.as_view()),
    path("admin/", admin.site.urls, name='adminURL'),
    # path("custom-admin/", custom_admin_site.urls),
    path("", include(('home.urls', 'app_name'), namespace="homeApplication")),
    path("auth/", include(('authenticationApp.urls.urls', 'app_name'), namespace="authenticationApplication")),
    path("staff/", include(('staffApp.urls.urls', 'app_name'), namespace="staffApplication")),
]

# Media File URL Configuration (in the development stage)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Customize Default Admin Panel
admin.site.index_title = "Integrated Budget & Accounting System"
admin.site.site_header = "iBAS++ Administration"
admin.site.site_title = "iBAS++ Administration"
