from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from ..forms import CustomerSupportRequestForm
from django.urls.base import reverse
from ..models import CustomerSupportRequest, CSOVisitorMessage, CSOVisitorConvoInfo
from authenticationApp.models import User
from datetime import date
import datetime
import uuid
from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


today = date.today()


# Landing Page View
class LangingPage(View):
    template_name = 'home/landingPage.html'
    form_class = CustomerSupportRequestForm
    context = {
        'title': 'Home',
    }
    def get(self, request):
        # self.context['form'] = self.form_class()
        print('#'*50)
        # print(f"Landing page form: { self.context['form'] }")
        # print('User session key:', request.session.session_key)
        if request.user.id == None:
            # print(request.user.id)
            # Check if the visitor has the "visitor_session_uuid" key in his/her session, otherwise create one.
            if 'visitor_session_uuid' in request.session:
                print('User session uuid:', request.session['visitor_session_uuid'])
            else:
                request.session['visitor_session_uuid'] = str(uuid.uuid4())
                print('Created a new session key-value pair! User session uuid:', request.session['visitor_session_uuid'])
            self.context['visitor_session_uuid'] = request.session['visitor_session_uuid']
        print('#'*50)
        return render(request, self.template_name, context=self.context)


class CustomerSupportRoom(View):
    """
    This class provides the CSO-Visitor-Chat platform for both the Customer Support Officer &
    the visitors.
    """
    template_name = 'home/customerSupport.html'
    context = {
        'title': 'Customer Support',
    }

    def get(self, request, *args, **kwargs):
        """
        Serves the CSO-visitor chat platform to both Customer Support Officer & The visitors.
        """
        self.context['room_slug'] = kwargs['room_slug']
        # print('Room Slug:', kwargs['room_slug'])
        if request.user.username != '':
            if request.user.is_cso:
                # Create CSOVisitorConvoInfo record here
                # check the chat support reqs of today
                print('today:', today)
                # conversations = CSOVisitorConvoInfo.objects.filter(created_at__contains=f'{today}')
                # conversations = CSOVisitorConvoInfo.objects.filter(created_at__date='2023-01-20')
                # conversations = CSOVisitorConvoInfo.objects.filter(created_at__day='20')
                # conversations = CSOVisitorConvoInfo.objects.filter(created_at__range=(datetime.date(2023,1,19), datetime.date(2023,1,20)))    # [WORKED]
                # conversations = CSOVisitorConvoInfo.objects.filter(created_at__range=(prev_day, today))   [WORKED]
                prev_day = today - datetime.timedelta(1)
                print('prev_day:', prev_day)
                print('CSO email:', request.user)
                # [First]: find if there is any such record existing in the table, 
                # since a cso might come to this same room multiple times, 
                # but that doesn't mean it'll create records everytime. 
                # It'll only create a record with 'is_connected=True' if no such record is found based on the following condition.
                # TODO: Once the conversation is resolved, redirect both the cso & visitor accordingly to cso-dashboard & homepage.
                # [{Edge-case - explaination for not using 'is_resolved=False' & 'is_connected=False' in the filter condition}: After the convo's being resolved, if the cso wants to re-visit the convo, don't create another convoInfo-record. Thus don't filter with 'is_resolved=False' as well as 'is_connected'=False, because 'is_connected'=False clause will hinder to find any such record & create a new record whenever the cso goes out the page & comes back during giving a resolution (bcz each record is created with 'is_connected'=True in the following creation-block). On the other hand, the 'is_resolved'=False will also hinder finding any such record & thus create another record if the CSO want to visit the room after making the 'is_resolved'=True by after giving the resolution.]
                conversations = CSOVisitorConvoInfo.objects.filter(
                    room_slug=kwargs['room_slug'],
                    cso_email=request.user.email,
                ).order_by('-created_at').first()
                print('\n'*3, '#'*50)
                print('conversations:', conversations)
                print('#'*50, '\n'*3)
                self.context['conversationInfo'] = conversations
                if conversations is not None:
                    print('conversations room slug:', conversations.room_slug, '------ email:', conversations.cso_email, '------ craeted at:', conversations.created_at)
                # for convo in conversations:
                #     print('conversations room slug:', convo.room_slug, '------ email:', convo.cso_email, '------ craeted at:', convo.created_at)
                # print(conversations is None)
                if conversations is None:
                    CSOVisitorConvoInfo.objects.create(
                        room_slug=kwargs['room_slug'], 
                        cso_email=request.user.email ,
                        is_connected=True,
                    )
        else:
            print('Anonymous User')
            # print('Anonymous user unique 32-char unique-code:', uuid.uuid4())
            # Attach the unique code to the users session as a new key-value pair

        
        # Get all the messages of that room_slug from the db
        messages = CSOVisitorMessage.objects.filter(room_slug=self.context['room_slug'])[:25]   # fetch the first 25 rows
        # for m in messages:
        #     print(m.user_identity)
        self.context['chat_messages'] = messages
        return render(request, self.template_name, context=self.context)
    
    # post-method: Only used by the CSO to make the convoInfo record's "is_resolved=True", "is_connected=False"
    def post(self, request, *args, **kwargs):
        """
        This post() method will make the "is_resolved=True", "is_connected=False" of the following convo-info-record.
        Then redirect the cso into his/her CSO-support-dashboard & the visitor into the homepage (through socket-connection).
        """
        room_slug = kwargs['room_slug']
        # TODO: Check if the "request.user" is cso.
        if request.user.is_cso:
            # TODO: Get the "convoInfo" record uisng "room_slug" & "cso_email". 
            # Check if the record of 'convoInfo' has the "is_connected=True" & "is_resolved=False", then only change the two-fields into vice-versa values.
            cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=room_slug, cso_email=request.user.email)
            # print('*'*50)            # print('convo is not resolved:', not cso_visitor_convo_info.is_resolved)            # print('convo is connected:', cso_visitor_convo_info.is_connected)            # print('*'*50)
            if (not cso_visitor_convo_info.is_resolved) and cso_visitor_convo_info.is_connected:
                cso_visitor_convo_info.is_resolved, cso_visitor_convo_info.is_connected = True, False
                cso_visitor_convo_info.save()
                # print('Change the record\'s field: "is_resolved=True" & "is_connected=False"')
                # # TODO: Send a signal to that socket-consumer about the chat-support is resolved.
                # channel_layer = get_channel_layer()
                # async_to_sync(channel_layer.group_send)(
                #     f'chat_{room_slug}',
                #     {
                #         'type': 'support_resolved',
                #         'cso_email': request.user.email
                #     }
                # )
        # TODO: Redirect the cso to his/her dashboard accordingly, then redirect the visitor to the homepage thorugh channel-connection automatic-btn-click with js from the visitor perspective in the "customerSupport.html" file.
        return redirect(reverse('staffApplication:CsoWorkload:SupportDashboard', kwargs={'email': request.user.email}))
        # return HttpResponse(f' \
        #     Will redirect the cso to his/her dashboard. room_slug: {room_slug} \
        #     cso email: {request.user.email}')


class CustomerSupportReq(View):
    """
    This class is used to handles the visitors' CSO-Support requests (creation), validation & 
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
        # TODO: Check if a request with the same visitor_session_uuid is already created.
        # [Concept - Storing visitor's uuid into his/her dj-session-key]:  https://www.youtube.com/watch?v=l5WZ_MlE14E&t=139s
        if 'visitorSessionUUID' in request.POST:
            # if found any, search for the room_slug in the "CustomerSupportRequest" model, if found then redirect the user to that room.
            visitor_support_req = CustomerSupportRequest.objects.filter(
                    visitor_session_uuid=request.POST['visitorSessionUUID'],
                ).order_by('-created_at').first()
            if visitor_support_req is not None:
                room_slug = visitor_support_req.room_slug
            else:
                client_ip, room_slug = request.POST['clientIP'], request.POST['roomSlug']
                CustomerSupportRequest.objects.create(
                    client_ip=client_ip,
                    visitor_session_uuid=request.POST['visitorSessionUUID'],
                    room_slug=room_slug,
                )

        return redirect(reverse(
            'homeApplication:CustomerSupportRoom', 
            kwargs={"room_slug": room_slug}
        ))
