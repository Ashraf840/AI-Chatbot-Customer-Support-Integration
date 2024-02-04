from django.db import models


class ChatbotVisitorMessage(models.Model):
    client_ip = models.CharField(max_length=20, blank=True, null=True)
    visitors_msg = models.CharField(max_length=255)
    bot_msg = models.CharField(max_length=255)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "Chatbot Visitor Message"


class CustomerSupportRequest(models.Model):
    client_ip = models.CharField(max_length=20, blank=True, null=True)
    room_slug = models.SlugField(unique=True)
    visitor_session_uuid = models.CharField(max_length=36, blank=True, null=True)   # uuid4 generated a string length of 36 chars
    registered_user_email = models.CharField(verbose_name='User Email', max_length=60, blank=True, null=True)
    registered_user_email_normalized = models.CharField(verbose_name='User Email (normalized)', max_length=60, blank=True, null=True)   # uuid4 generated a string length of 36 chars
    assigned_cso = models.CharField(verbose_name="Assigned HDO", max_length=60, blank=True, null=True)
    is_resolved = models.BooleanField(default=False, help_text="Marked as resolved if the HDO marked the coordinating convoInfo as resolved")
    is_dismissed = models.BooleanField(verbose_name="Dismissed", default=False, help_text="Mark as dismissed if the HDO marked the coordinating convoInfo as dismissed")
    is_detached = models.BooleanField(verbose_name="Detached", default=False, help_text="Mark as detached if the HDO mark the 'CustomerSupportRequest' as resolved or dismissed")
    issue_by_oid = models.CharField(max_length=60, blank=True, null=True, default='6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac', help_text='Remove the default oid later (when the bot will create the issue & get the response)')
    chatbot_socket_id = models.CharField(max_length=60, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "HDO Support Request"

    @staticmethod
    def get_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal_post_save" func, so that whenever a record is created, the signal can use this func to get all the records (updated) from the table
        """
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'registered_user_email_normalized', 'is_resolved', 'is_dismissed', 'is_detached', 'issue_by_oid', 'assigned_cso'))
        instances = [x for x in instances if not x['is_detached']]
        return instances

    @staticmethod
    def get_unresolved_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal_post_save" func, so that whenever a record is resolved, the signal can use this func to get all the unresolved records (updated) from the table
        """
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email_normalized', 'is_resolved', 'issue_by_oid', 'assigned_cso'))
        result = [x for x in instances if not x['is_resolved']]
        return result

    @staticmethod
    def get_reqs_with_creation_timestamp(cso_email=None):
        result = []
        if cso_email is None:
            instances = CustomerSupportRequest.objects.values(
                'assigned_cso', 'is_detached', 'created_at'
            ).order_by('-id')
            for i in instances:
                if i['assigned_cso'] is not None and not i['is_detached']:
                    result.append(i)
        else:
            instances = CustomerSupportRequest.objects.filter(assigned_cso=cso_email).values(
                'assigned_cso', 'is_detached', 'created_at'
            ).order_by('-id')
            for i in instances:
                if not i['is_detached']:
                    result.append(i)
        return result

    @staticmethod
    def get_reqs_with_assigned_cso(cso_email=None):
        """
        This method will return the assigned message requests. 
        This method is also used for getting curated message-requests according to the cso_emails if provided while invoking the method.
        """
        result = []
        if cso_email is None:
            instances = CustomerSupportRequest.objects.values(
                'client_ip', 'room_slug', 'visitor_session_uuid', 
                'registered_user_email', 'registered_user_email_normalized', 'assigned_cso', 
                'issue_by_oid', 'is_detached', 'created_at').order_by('-id')
            
            for i in instances:
                if i['assigned_cso'] is not None and not i['is_detached']:
                    result.append(i)
        else:
            instances = CustomerSupportRequest.objects.filter(assigned_cso=cso_email).values(
                'client_ip', 'room_slug', 'visitor_session_uuid', 
                'registered_user_email', 'registered_user_email_normalized', 'assigned_cso', 
                'issue_by_oid', 'is_detached', 'created_at').order_by('-id')
            
            for i in instances:
                if not i['is_detached']:
                    result.append(i)
        return result


    def save(self, *args, **kwargs):
        if not self.is_detached:
            if self.is_resolved or self.is_dismissed:
                self.is_detached = True
        super(CustomerSupportRequest, self).save(*args, **kwargs)

# Store each message of both a CSO & a visitor
class CSOVisitorMessage(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    user_identity = models.CharField(max_length=25)
    room_slug = models.CharField(max_length=25)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "HDO Visitor Messages"


class CSOVisitorConvoInfo(models.Model):
    """
    This class model stores conversations of both CSO-visitor & CSO-user. 
    Only for anonymous users, the conversations are fetched based on room-slug value.
    """
    room_slug = models.CharField(max_length=25)
    cso_email = models.CharField(max_length=60, verbose_name='Help Desk Officer Email')
    registered_user_email = models.CharField(verbose_name='User Email', max_length=60, blank=True, null=True)
    is_resolved = models.BooleanField(default=False, help_text="HDO marks the issue as resolved, displays boolean values")
    is_dismissed = models.BooleanField(default=False, help_text="HDO marks the issue as dismissed, displays boolean values")
    is_connected = models.BooleanField(verbose_name='Is HDO connected?', default=False, help_text="The HDO has marked this conversation as resolved if it's displayed 'False'")
    issue_by_oid = models.CharField(max_length=60, blank=True, null=True, default='6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac', help_text='Remove the default oid later (when the bot will create the issue & add value from "CustomerSupportRequest()" model)')
    is_cancelled = models.BooleanField(verbose_name='Chat cancelled', default=False, help_text="The user cancelled the chat-conversation, thus the associate msg-req will be removed form the CSR list")
    is_cleared = models.BooleanField(verbose_name='Associate msg-req is removed', default=False, help_text="The HDO removed/cleared the associate msg-req from the CSR List, thus the conversation will be marked as cleared")
    created_at = models.DateTimeField(verbose_name="Conversation created at", auto_now=True)

    class Meta:
        verbose_name_plural = "HDO Visitor Conversation Information"
    
    @staticmethod
    def get_unresolved_msg():
        """
        This method will get the curated messages which are not resolved yet.
        """
        instances = list(CSOVisitorConvoInfo.objects.values('room_slug', 'cso_email', 'is_resolved', 'is_connected'))
        result = []
        for msgInfo in instances:
            if not msgInfo['is_resolved']:
                result.append(msgInfo)
        return result


class UserChatbotSocket(models.Model):
    """
    This class model stores user-email along with the chatbot's unique socket-id. 
    """
    user_email = models.CharField(max_length=60)
    chatbot_socket_id = models.CharField(max_length=60, verbose_name='Chatbot Socket Unique ID')
    registered_user_session_uuid = models.CharField(max_length=60, verbose_name='Registered User Session UUID')
    created_at = models.DateTimeField(verbose_name="Chatbot Socket Record Created At", auto_now_add=True)


class RemarkResolution(models.Model):
    """
    This class model stores remarks & resolution of each CSO-User Conversation
    """
    cso_user_convo = models.ForeignKey(CSOVisitorConvoInfo, verbose_name='HDO-User Conversation', on_delete=models.DO_NOTHING)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created remarks after providing solution", auto_now_add=True)












