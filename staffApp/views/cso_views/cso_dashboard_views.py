from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import CustomerSupportRequest
from authenticationApp.models import User
from ...cso_connectivity_models import CSOOnline


# TODO: [Done] Create cso dashboard class
class CsoDashboard(LoginRequiredMixin, View):
    # Solution Ref: https://stackoverflow.com/a/68433938
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'CSO Dashboard',
    }

    def get(self, request):
        return render(request, 'staffApp/cso/cso_dashboard.html', self.context)


class SupportDashboard(LoginRequiredMixin, View):
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'Support Dashboard',
    }

    def get(self, request, email):
        # Get all the customer-support-req data from "CustomerSupportRequest" model
        # --------------------------------------------------------------------------------
        user = get_object_or_404(User, email=email)
        customer_support_requests = CustomerSupportRequest.objects.all().order_by('-id')
        print(f"'SupportDashboard' class queryset: {customer_support_requests}")
        print(f"total support requests: {len(customer_support_requests)}")
        self.context['support_req_nums'] = len(customer_support_requests)
        self.context['customer_support_requests'] = customer_support_requests
        self.context['cso_email'] = request.user.email
        # --------------------------------------------------------------------------------
        return render(request, 'staffApp/cso/support_dashboard.html', self.context)


class SupportDashboardNew(LoginRequiredMixin, View):
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'Support Dashboard',
    }

    def get(self, request, email):
        user = get_object_or_404(User, email=email)
        customer_support_requests = CustomerSupportRequest.objects.all().order_by('-id')
        print(f"'SupportDashboard' class queryset: {customer_support_requests}")
        print(f"total support requests: {len(customer_support_requests)}")
        self.context['support_req_nums'] = len(customer_support_requests)
        self.context['customer_support_requests'] = customer_support_requests
        self.context['cso_email'] = request.user.email
        # --------------------------------------------------------------------------------
        return render(request, 'staffApp/cso/support_dashboard_newUI.html', self.context)



class CSOOnlineConnectivityDashboard(LoginRequiredMixin, View):
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'CSO Online Connectivity Dashboard',
    }

    def get(self, request):
        cso_online = CSOOnline.objects.all().order_by('-id')
        self.context['cso_online'] = cso_online
        return render(request, 'staffApp/cso/cso_online_connectivity_dashboard.html', self.context)

