from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import CustomerSupportRequest

# TODO: [Done] Create cso dashboard class
class CsoDashboard(LoginRequiredMixin, View):
    # Solution Ref: https://stackoverflow.com/a/68433938
    login_url = 'authenticationApplication:CsoAuth:CSOLoginPageView'
    context = {
        'title': 'CSO Dashboard',
    }

    def get(self, request):
        # Get all the customer-support-req data from "CustomerSupportRequest" model
        customer_support_requests = CustomerSupportRequest.objects.all().order_by('-id')
        print(f"'CsoDashboard' class queryset: {customer_support_requests}")
        print(f"total support requests: {len(customer_support_requests)}")
        self.context['support_req_nums'] = len(customer_support_requests)
        sample = [i for i in range(2)]
        self.context['sample_row'] = sample
        self.context['customer_support_requests'] = customer_support_requests
        return render(request, 'staffApp/cso/dashboard.html', self.context)
