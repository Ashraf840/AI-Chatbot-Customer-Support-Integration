from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import CustomerSupportRequest
from authenticationApp.models import User, User_signin_token_tms
from ...cso_connectivity_models import CSOOnline
from django.urls.base import reverse
from authenticationApp.utils.userDetail import UserDetail


# TODO: [Done] Create cso dashboard class
class CsoDashboard(LoginRequiredMixin, View):
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'Help Desk Dashboard',
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

        usr_detail = UserDetail(user_email=request.user.email)
        usr_profile = usr_detail.user_profile_detail(request.user.email)
        user_organization, user_location, user_district, user_division = usr_profile.user_organization, usr_profile.location, usr_profile.district, usr_profile.division
        self.context['user_organization'] = user_organization
        self.context['user_location'] = user_location
        self.context['user_district'] = user_district
        self.context['user_division'] = user_division
        # --------------------------------------------------------------------------------
        return render(request, 'staffApp/cso/support_dashboard.html', self.context)
    
    def post(self, request, email):
        cso_email = request.POST['cso_email']
        room_slug = request.POST['room_slug']
        print('\n'*3, '$'*50)
        print(f'CSO email: {cso_email}; Room slug: {room_slug}')
        print('\n'*3, '$'*50)
        try:
            msg_req = CustomerSupportRequest.objects.get(assigned_cso=cso_email, room_slug=room_slug)
            msg_req.delete()
        except:
            return redirect(reverse(
                'staffApplication:CsoWorkload:SupportDashboard', 
                kwargs={"email": cso_email}
            ))
        # return reverse('staffApplication:CsoWorkload:SupportDashboard', kwargs={'email': cso_email})
        return redirect(reverse(
            'staffApplication:CsoWorkload:SupportDashboard', 
            kwargs={"email": cso_email}
        ))



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

