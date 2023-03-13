from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import CustomerSupportRequest
from authenticationApp.models import User, User_signin_token_tms
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
        # user = get_object_or_404(User, email=email)
        # customer_support_requests = CustomerSupportRequest.objects.all().order_by('-id')  # get all the msg-reqs in descending order of the 'created_at' field
        customer_support_requests = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=email)

        try:
            user_signing_token_tms = User_signin_token_tms.objects.get(user_email=email)
            self.context['user_signing_token_tms'] = user_signing_token_tms.user_token;
        except User_signin_token_tms.DoesNotExist:
            # TODO: Logout the user & prompt the CSO to login into the system again
            # TODO: Provide a flash-msg afterwards the CSO is logged out & redirected to the login page. ("TMS authentication-token is expired")
            return redirect('authenticationApplication:CsoAuth:CSOLogoutView')
        # cso_user_chat_info = CSOVisitorConvoInfo.get_unresolved_msg()
        # room_tuple = tuple([r['room_slug'] for r in cso_user_chat_info])
        # unresolved_total_msg = []
        # for csr in customer_support_requests:
        #     if csr['room_slug'] in room_tuple:
        #         unresolved_total_msg.append(csr)
        
        # customer_support_requests = unresolved_total_msg
        print(f"'SupportDashboard' class queryset: {customer_support_requests}")
        print(f"total support requests: {len(customer_support_requests)}")
        self.context['support_req_nums'] = len(customer_support_requests)
        self.context['customer_support_requests'] = customer_support_requests
        self.context['cso_email'] = request.user.email
        # --------------------------------------------------------------------------------
        return render(request, 'staffApp/cso/support_dashboard.html', self.context)


# NOT USING CURRENTLY
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
        self.context['cso_online_offline'] = cso_online
        self.context['cso_online'] = len(CSOOnline.get_active_cso())
        return render(request, 'staffApp/cso/cso_online_connectivity_dashboard.html', self.context)

