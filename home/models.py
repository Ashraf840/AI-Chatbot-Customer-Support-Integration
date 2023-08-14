from django.db import models
# from authenticationApp.models import User     [ not using since mongodb cannot work with Foreignkey fields ]
# from djongo import models as djongo_models    # [ Djongo-type models - not using since the entire existing models need to be build using djongo-type-model lib, otherwise it'll not incorporate with typical-django-models lib ]



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
    registered_user_email = models.CharField(verbose_name='User Email', max_length=60, blank=True, null=True)   # uuid4 generated a string length of 36 chars
    registered_user_email_normalized = models.CharField(verbose_name='User Email (normalized)', max_length=60, blank=True, null=True)   # uuid4 generated a string length of 36 chars
    assigned_cso = models.CharField(verbose_name="Assigned HDO", max_length=60, blank=True, null=True)
    is_resolved = models.BooleanField(verbose_name="Resolved", default=False, help_text="Mark as resolved if the HDO marked the coordinating convoInfo as resolved")
    is_dismissed = models.BooleanField(verbose_name="Dismissed", default=False, help_text="Mark as dismissed if the HDO marked the coordinating convoInfo as dismissed")
    is_detached = models.BooleanField(verbose_name="Detached", default=False, help_text="Mark as detached if the HDO mark the 'CustomerSupportRequest' as resolved or dismissed")
    issue_by_oid = models.CharField(max_length=60, blank=True, null=True, default='6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac', help_text='Remove the default oid later (when the bot will create the issue & get the response)')
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        # verbose_name_plural = "Customer Support Request"
        verbose_name_plural = "HDO Support Request"

    @staticmethod
    def get_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal_post_save" func, so that whenever a record is created, the signal can use this func to get all the records (updated) from the table which are not detached yet (is_detached=False).
        """
        # instances = CustomerSupportRequest.objects.all()
        # instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email_normalized', 'is_resolved', 'issue_by_oid', 'assigned_cso'))   # Solution: https://stackoverflow.com/a/7811582
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'registered_user_email_normalized', 'is_resolved', 'is_dismissed', 'is_detached', 'issue_by_oid', 'assigned_cso', 'created_at'))   # NB: currently not necessary to display visitor's-session-uuid
        # instances = [x for x in instances if not x['is_resolved']]
        # instances = [x for x in instances if not x['is_resolved'] or not x['is_dismissed']]     # pick issue-reqs that aren't resolved nor dismissed
        instances = [x for x in instances if not x['is_detached']]     # pick issue-reqs that aren't detached yet due to mark as resolved/dismissed
        # instances = list(map(lambda x: not x['is_resolved'] or not x['is_dismissed']))
        # instances = [x for x in instances if not x.get('is_resolved') or not x.get('is_dismissed')]
        # letters = list(map(lambda x: x, 'human'))
        # x = list(map(lambda x: not x['is_resolved'] or not x['is_dismissed'], instances))
        return instances

    @staticmethod
    def get_unresolved_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal_post_save" func, so that whenever a record is resolved, the signal can use this func to get all the unresolved records (updated) from the table
        """
        # instances = CustomerSupportRequest.objects.all()
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email_normalized', 'is_resolved', 'issue_by_oid', 'assigned_cso'))   # Solution: https://stackoverflow.com/a/7811582
        result = [x for x in instances if not x['is_resolved']]
        return result

    @staticmethod
    def get_reqs_with_creation_timestamp(cso_email=None):
        result = []
        if cso_email is None:
            # Get all msg-reqs' timestamps in descending order (latest to oldest)
            instances = CustomerSupportRequest.objects.values(
                'assigned_cso', 'is_detached', 'created_at'
            ).order_by('-id')
            for i in instances:
                if i['assigned_cso'] is not None and not i['is_detached']:
                    result.append(i)
        else:
            # Get a particular HDO's all the msg-reqs' timestamps in descending order (latest to oldest)
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
        # instances = CustomerSupportRequest.objects.all()
        result = []
        if cso_email is None:
            instances = CustomerSupportRequest.objects.values(
                'client_ip', 'room_slug', 'visitor_session_uuid', 
                'registered_user_email_normalized', 'assigned_cso', 
                'issue_by_oid', 'is_detached', 'created_at').order_by('-id')
            
            # print(f"message-req-instances (assigned-cso-email is empty): {instances}")
            for i in instances:
                # if i['assigned_cso'] is not None and not i['is_resolved']:
                if i['assigned_cso'] is not None and not i['is_detached']:
                    result.append(i)
        else:
            instances = CustomerSupportRequest.objects.filter(assigned_cso=cso_email).values(
                'client_ip', 'room_slug', 'visitor_session_uuid', 
                'registered_user_email_normalized', 'assigned_cso', 
                'issue_by_oid', 'is_detached', 'created_at').order_by('-id')
            
            # print(f"message-req-instances (assigned-cso-email is not empty): {instances}")
            for i in instances:
                # if i['assigned_cso'] == cso_email and not i['is_resolved']:
                # if i['assigned_cso'] == cso_email and not i['is_detached']:
                if not i['is_detached']:
                    result.append(i)
        # print("get_reqs_with_assigned_cso.appendedInstances:", result)
        # print("get_reqs_with_assigned_cso.appendedInstances length:", len(result))
        return result

    # https://stackoverflow.com/questions/53461830/send-message-using-django-channels-from-outside-consumer-class

    # group-send about all the support-request-query from this model's signal (post_save) to "CSODashboardConsumer" consumer.

    def save(self, *args, **kwargs):
        # Check if the record is previously detached or not
        if not self.is_detached:
            # For both resolve/dismiss, the req will be detached
            if self.is_resolved or self.is_dismissed:
                print("Mark the request as 'is_detached=True'!")
                self.is_detached = True
        # TODO: Remove the "else-code-block". [Explanation] Because it causes problem: if admin wants to re-mark an issue as dismissed which is already resolved, then this else-code-block again mark the issue as "detached=False" along with "dismissed=True". Vice-Versa scenario is applicable.
        # else:
        #     if not self.is_resolved or not self.is_dismissed:
        #         print("Mark the request as 'is_detached=False'!")
        #         self.is_detached = False
        super(CustomerSupportRequest, self).save(*args, **kwargs)


# Store each message of both a CSO & a visitor
class CSOVisitorMessage(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    user_identity = models.CharField(max_length=25)
    room_slug = models.CharField(max_length=25)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        # verbose_name_plural = "CSO Visitor Messages"
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
    is_connected = models.BooleanField(verbose_name='Is HDO connected?', default=False, help_text="The HDO has marked this conversation as resolved/dismissed if it's displayed 'False'")
    issue_by_oid = models.CharField(max_length=60, blank=True, null=True, default='6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac', help_text='Remove the default oid later (when the bot will create the issue & add value from "CustomerSupportRequest()" model)')
    is_cancelled = models.BooleanField(verbose_name='Chat cancelled', default=False, help_text="The user cancelled the chat-conversation, thus the associate msg-req will be removed form the CSR list")
    is_cleared = models.BooleanField(verbose_name='Associate msg-req is removed', default=False, help_text="The HDO removed/cleared the associate msg-req from the CSR List, thus the conversation will be marked as cleared")
    created_at = models.DateTimeField(verbose_name="Conversation created at", auto_now=True)

    class Meta:
        # verbose_name_plural = "CSO Visitor Conversation Information"
        verbose_name_plural = "HDO Visitor Conversation Information"
    
    @staticmethod
    def get_unresolved_msg():
        """
        This method will get the curated messages which are not resolved yet.
        """
        # instances = CustomerSupportRequest.objects.all()
        instances = list(CSOVisitorConvoInfo.objects.values('room_slug', 'cso_email', 'is_resolved', 'is_connected'))   # Solution: https://stackoverflow.com/a/7811582
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
    created_at = models.DateTimeField(verbose_name="Chatbot Socket Record Created At", auto_now_add=True)    #Add date-time automaticate when a record is created into this table



class RemarkResolution(models.Model):
    """
    This class model stores remarks & resolution of each CSO-User Conversation
    """
    cso_user_convo = models.ForeignKey(CSOVisitorConvoInfo, verbose_name='HDO-User Conversation', on_delete=models.DO_NOTHING)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created remarks after providing solution", auto_now_add=True)
