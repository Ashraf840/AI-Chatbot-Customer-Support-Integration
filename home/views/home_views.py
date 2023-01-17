from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from ..forms import CustomerSupportRequestForm
from django.urls.base import reverse
from ..models import CustomerSupportRequest, CSOVisitorMessage


# def homePage(request):
#     context = {
#         'title': 'Dhaka Residential Model College',
#     }
#     return render(request, 'home/index.html' , context)


# Landing Page View
class LangingPage(View):
    form_class = CustomerSupportRequestForm
    context = {
        'title': 'Home',
    }
    def get(self, request):
        # self.context['form'] = self.form_class()
        # print('#'*50)
        # print(f"Landing page form: { self.context['form'] }")
        # print('#'*50)
        return render(request, 'home/landingPage.html', context=self.context)


class CustomerSupportRoom(View):
    """
    This class provides the CSO-Visitor-Chat platform for both Customer Support Officer &
    The visitors.
    """
    template_name = 'home/customerSupport.html'
    context = {
        'title': 'Customer Support',
    }

    def get(self, request, *args, **kwargs):
        """
        Serves the CSO-visistor chat platform to both Customer Support Officer & The visitors.
        """
        self.context['room_slug'] = kwargs['room_slug']

        
        # Get all the messages of that room_slug from the db
        messages = CSOVisitorMessage.objects.filter(room_slug=self.context['room_slug'])[:25]   # fetch the first 25 rows
        for m in messages:
            print(m.user_identity)
        self.context['chat_messages'] = messages
        return render(request, self.template_name, context=self.context)


class CustomerSupportReq(View):
    """
    This class is used to handles thr visitors' CSO-Support connection request, validation & 
    later rediects them to the CSO-Visitor-Chat platform through "CustomerSupportRoom" class.
    """
    context = {
        'title': 'Customer Support',
    }
    def post(self, request):
        """
        This "post()" method will be used from chat-window panel's connect button, 
        thus the visitors can access the customer-support-chat room.
        """
        # print("Backend 'CustomerSupportRoom' class post method.")
        # print(f"Client IP: {request.POST['clientIP']}")
        # print(f"Room Slug: {request.POST['roomSlug']}")
        
        # TODO: store the support-req data into a DB table ("CustomerSupportRequest");
        client_ip, room_slug = request.POST['clientIP'], request.POST['roomSlug']
        CustomerSupportRequest.objects.create(
            client_ip=client_ip,
            room_slug=room_slug
        )
        return redirect(reverse(
            'homeApplication:CustomerSupportRoom', 
            kwargs={"room_slug": request.POST['roomSlug']}
        ))
