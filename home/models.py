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
    registered_user_email_normalized = models.CharField(verbose_name='User Email (normalized)', max_length=60, blank=True, null=True)   # uuid4 generated a string length of 36 chars
    assigned_cso = models.CharField(max_length=60, blank=True, null=True)
    is_resolved = models.BooleanField(default=False, help_text="Marked as resolved if the CSO marked the coordinating convoInfo as resolved")
    issue_by_oid = models.CharField(max_length=60, blank=True, null=True, default='6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac', help_text='Remove the default oid later (when the bot will create the issue & get the response)')
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "Customer Support Request"

    @staticmethod
    def get_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal" func, so that whenever a record is created, the signal can use this func to get all the records (updated) from the table
        """
        # instances = CustomerSupportRequest.objects.all()
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email_normalized', 'issue_by_oid', 'assigned_cso'))   # Solution: https://stackoverflow.com/a/7811582
        return instances

    @staticmethod
    def get_reqs_with_assigned_cso(cso_email=None):
        """
        This method will return the assigned message requests. 
        This method is also used for getting curated message-requests according to the cso_emails if provided while invoking the method.
        """
        # instances = CustomerSupportRequest.objects.all()
        instances = CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email_normalized', 'assigned_cso', 'is_resolved', 'created_at').order_by('-id')
        print(f"message-req-instances: {instances}")
        result = []
        if cso_email is None:
            for i in instances:
                if i['assigned_cso'] is not None and not i['is_resolved']:
                    result.append(i)
        else:
            for i in instances:
                if i['assigned_cso'] == cso_email and not i['is_resolved']:
                    result.append(i)
        return result

    # https://stackoverflow.com/questions/53461830/send-message-using-django-channels-from-outside-consumer-class

    # group-send about all the support-request-query from this model's signal (post_save) to "CSODashboardConsumer" consumer.


# Store each message of both a CSO & a visitor
class CSOVisitorMessage(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    user_identity = models.CharField(max_length=25)
    room_slug = models.CharField(max_length=25)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "CSO Visitor Messages"


class CSOVisitorConvoInfo(models.Model):
    """
    This class model stores conversations of both CSO-visitor & CSO-user. 
    Only for anonymous users, the conversations are fetched based on room-slug value.
    """
    room_slug = models.CharField(max_length=25)
    cso_email = models.CharField(max_length=60, verbose_name='Customer Support Officer Email')
    registered_user_email = models.CharField(verbose_name='User Email', max_length=60, blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    is_connected = models.BooleanField(verbose_name='Is CSO connected?', default=False, help_text="The CSO has marked this conversation as resolved if it's displayed 'False'")
    created_at = models.DateTimeField(verbose_name="Conversation created at", auto_now=True)

    class Meta:
        verbose_name_plural = "CSO Visitor Conversation Information"
    
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
