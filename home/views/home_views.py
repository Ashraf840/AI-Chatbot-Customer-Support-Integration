from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from ..forms import CustomerSupportRequestForm
from django.urls.base import reverse
from ..models import CustomerSupportRequest, CSOVisitorMessage, CSOVisitorConvoInfo
from authenticationApp.models import User, User_Profile
from authenticationApp.utils.userDetail import UserDetail
from datetime import date
import datetime
import uuid, psycopg2
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from asgiref.sync import async_to_sync
from authenticationApp.models import User_Profile, User_signin_token_tms


today = date.today()


class LangingPage(LoginRequiredMixin, View):
    login_url = 'authenticationApplication:UserAuth:UserLoginPageView'
    template_name = 'home/Chatbot-Widget-IBAS/landingPage.html'
    form_class = CustomerSupportRequestForm
    context = {
        'title': 'Home',
    }
    def get(self, request):
        print('#'*50)
        if request.user.id == None:
            if 'visitor_session_uuid' in request.session:
                print('User session uuid:', request.session['visitor_session_uuid'])
            else:
                request.session['visitor_session_uuid'] = str(uuid.uuid4())
                print('Created a new session key-value pair! User session uuid:', request.session['visitor_session_uuid'])
            self.context['visitor_session_uuid'] = request.session['visitor_session_uuid']
        else:
            print(f"User Id: {request.user.id}")
            usremail_normalized="".join(uemail for uemail in request.user.email if uemail.isalnum())

            usr_detail = UserDetail(user_email=request.user.email)
            usr_profile = usr_detail.user_profile_detail(request.user.email)
            user_organization, user_location, user_district, user_division = usr_profile.user_organization, usr_profile.location, usr_profile.district, usr_profile.division
            self.context['user_organization'] = user_organization
            self.context['user_location'] = user_location
            self.context['user_district'] = user_district
            self.context['user_division'] = user_division

            self.context['user_email'] = request.user.email
            self.context['user_email_normalized'] = usremail_normalized
            request.session['registered_user_session_uuid'] = str(uuid.uuid4())
            self.context['registered_user_session_uuid'] = request.session['registered_user_session_uuid']
        print('#'*50)
        return render(request, self.template_name, context=self.context)


class CustomerSupportRoom(View):
    """
    This class provides the CSO-Visitor-Chat platform for both the Customer Support Officer &
    the visitors.
    """
    login_url = 'authenticationApplication:UserAuth:UserLoginPageView'
    template_name = 'home/customerSupport.html'
    context = {
        'title': 'Help Desk Chatroom',
    }

    def get(self, request, *args, **kwargs):
        """
        Serves the CSO-visitor chat platform to both Customer Support Officer & The visitors.
        """
        self.context['room_slug'] = kwargs['room_slug']
        if request.user.username != '':
            if request.user.is_cso:
                print('today:', today)
                prev_day = today - datetime.timedelta(1)
                print('prev_day:', prev_day)
                print('CSO email:', request.user)
                conversations = CSOVisitorConvoInfo.objects.filter(
                    room_slug=kwargs['room_slug'],
                ).order_by('-created_at').first()
                print('\n'*3, '#'*50)
                print('conversations:', conversations)
                print('#'*50, '\n'*3)
                self.context['conversationInfo'] = conversations
                self.context['chat_convo_cancelled'] = conversations.is_cancelled
                if conversations is not None:
                    print('conversations room slug:', conversations.room_slug, '------ email:', conversations.cso_email, '------ craeted at:', conversations.created_at)
                    conversations.cso_email = request.user.email
                    conversations.is_connected = True
                    conversations.save()
                if conversations is None:
                    conversations = CSOVisitorConvoInfo.objects.create(
                        room_slug=kwargs['room_slug'], 
                        cso_email=request.user.email ,
                        is_connected=True,
                    )
                csoEmail = conversations.cso_email
                registeredUserEmail = conversations.registered_user_email
                print(f'CSO Visitor Convo Info: {registeredUserEmail}')
                registeredUser_record = User.objects.get(email=registeredUserEmail)
                self.context['registered_user_fullname'] = registeredUser_record.first_name + ' ' + registeredUser_record.last_name
                self.context['registered_user_email'] = registeredUser_record.email
                self.context['registered_user_phone'] = registeredUser_record.phone
                self.context['registered_user_profile_pic'] = registeredUser_record.profile_pic

                self.context['common_cso_email'] = csoEmail
                self.context['common_registered_user_email'] = registeredUserEmail

                tms_issue_by_oid = conversations.issue_by_oid
                self.context['tms_issue_by_oid'] = tms_issue_by_oid

                csr_record = CustomerSupportRequest.objects.get(room_slug=conversations.room_slug)
                self.context['chatbot_socket_id'] = csr_record.chatbot_socket_id

                try:
                    userName_bn = User_Profile.objects.get(user_email=registeredUserEmail)
                    print(userName_bn.user_name_bn)
                    if not userName_bn.user_name_bn is None:
                        print('Username is not none!')
                        self.context['userName_bn'] = userName_bn.user_name_bn
                    else:
                        print('Username is none!')
                        self.context['userName_bn'] = 'null'
                except User_Profile.DoesNotExist:
                    print('User profile does not exist!')
                    self.context['userName_bn'] = 'null'
                

                try:
                    user_signing_token_tms = User_signin_token_tms.objects.get(user_email=request.user.email)
                    self.context['user_signing_token_tms'] = user_signing_token_tms.user_token
                except User_signin_token_tms.DoesNotExist:
                    return redirect('authenticationApplication:CsoAuth:CSOLogoutView')
            
            if request.user.is_user:
                conversations = CSOVisitorConvoInfo.objects.filter(
                    room_slug=kwargs['room_slug'],
                ).order_by('-created_at').first()
                self.context['conversationInfo'] = conversations

                if conversations is not None:
                    conversations.registered_user_email = request.user.email
                    conversations.save()
                    print('conversations room slug:', conversations.room_slug, '------ email:', conversations.registered_user_email, '------ craeted at:', conversations.created_at)
                if conversations is None:
                    conversations = CSOVisitorConvoInfo.objects.create(
                        room_slug=kwargs['room_slug'], 
                        registered_user_email=request.user.email,
                    )
                
                csr_record = CustomerSupportRequest.objects.get(room_slug=conversations.room_slug)
                cso_user_email = csr_record.assigned_cso
                tms_issue_by_oid = csr_record.issue_by_oid
                self.context['tms_issue_by_oid'] = tms_issue_by_oid
                self.context['chatbot_socket_id'] = csr_record.chatbot_socket_id
                csoEmail = cso_user_email
                registeredUserEmail = conversations.registered_user_email
                self.context['common_cso_email'] = csoEmail
                self.context['common_registered_user_email'] = registeredUserEmail
                user_signing_token_tms = User_signin_token_tms.objects.get(user_email=csr_record.assigned_cso)
                self.context['user_signing_token_tms'] = user_signing_token_tms.user_token
                conversations.issue_by_oid=csr_record.issue_by_oid
                conversations.save()

                try:
                    cso_user_record = User.objects.get(email=cso_user_email)
                    self.context['cso_user_fullname'] = cso_user_record.first_name + ' ' + cso_user_record.last_name
                    self.context['cso_user_email'] = cso_user_email
                    self.context['cso_user_phone'] = cso_user_record.phone
                    self.context['cso_user_profile_pic'] = cso_user_record.profile_pic
                except:
                    self.context['cso_user_fullname'] = 'null'
                    self.context['cso_user_email'] = 'null'
                    self.context['cso_user_phone'] = 'null'
                    self.context['cso_user_profile_pic'] = 'null'
        else:
            print('Anonymous User')

        print("csr_record.chatbot_socket_id:", csr_record.chatbot_socket_id)
        
        # Raw query to get all the requests from "event" table
        try:
            conn = psycopg2.connect(
                dbname="ibas_db",
                user="ibas_admin",
                password="L10w$ShRU021",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            sql_query = f"SELECT type_name, (data::json)->>'text' FROM public.events WHERE sender_id='{csr_record.chatbot_socket_id}' AND type_name='user' OR type_name='bot';"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            results = [(row[0], row[1][:-1]) for row in results]
            conn.commit()
            cursor.close()
            conn.close()
            repeat_counter, polished_results = 0, []

            for row in results[11:]:
                if repeat_counter <=3:
                    if row[1]=="দুঃখিত, আপনার সমস্যাটি এই মুহুর্তে সমাধান করা সম্ভব হচ্ছে না, আমাদের প্রতিনিধি খুব শীঘ্রই বিষয়টি নিয়ে আপ্নার সাথে যোগাযোগ করবেন" or \
                        row[1]=="আপনার সমস্যাটির শ্রেণী নির্বাচন করুনঃ" or \
                            row[1]=="আপনার সমসস্যাটি আমাদের অবগত করার জন্য ধন্যবাদ, শীঘ্রই আমাদের প্রতিনিধি আপনার সাথে যোগাযোগ করবেন":
                            repeat_counter+=1
                            continue
                if row[0]=="bot":
                    # print("Left side:", row[1])
                    polished_results.append(row)
                if row[0]=="user":
                    # print("Right side:", row[1])
                    polished_results.append(row)
            self.context['chatbot_history'] = polished_results
        except:
            pass
        messages = CSOVisitorMessage.objects.filter(room_slug=self.context['room_slug'])
        self.context['chat_messages'] = messages
        return render(request, self.template_name, context=self.context)



def createCustomerSupportRequest(visitorSessionUUID=None, user_email=None):
    if visitorSessionUUID != None:
        pass
    if user_email != None:
        pass
    pass


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
        if 'visitorSessionUUID' in request.POST:
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
        if 'user_email_normalized' in request.POST:
            # chatbot_socket_id
            client_ip, room_slug, ticketIssuerOid, user_email, chatbotSocketId \
                = request.POST['clientIP'], request.POST['roomSlug'], request.POST['ticketIssuerOid'], request.POST['user_email'], request.POST['chatbotSocketId']
            CustomerSupportRequest.objects.create(
                client_ip=client_ip,
                registered_user_email=user_email,
                registered_user_email_normalized=request.POST['user_email_normalized'],
                room_slug=room_slug,
                issue_by_oid=ticketIssuerOid,
                chatbot_socket_id=chatbotSocketId,
            )
    
        return redirect(reverse(
            'homeApplication:CustomerSupportRoom', 
            kwargs={"room_slug": room_slug}
        ))
