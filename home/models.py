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
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "Customer Support Request"

    @staticmethod
    def get_customer_support_reqs():
        """
        This method is used in the signals.py file's "customer_support_request_signal" func, so that whenever a record is created, the signal can use this func to get all the records (updated) from the table
        """
        # instances = CustomerSupportRequest.objects.all()
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug', 'visitor_session_uuid'))   # Solution: https://stackoverflow.com/a/7811582
        return instances

    # https://stackoverflow.com/questions/53461830/send-message-using-django-channels-from-outside-consumer-class

    # group-send about all the support-request-query from this model's signal (post_save) to "CSODashboardConsumer" consumer.


class CSOVisitorMessage(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True)
    user_identity = models.CharField(max_length=25)
    room_slug = models.CharField(max_length=25)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "CSO Visitor Messages"


class CSOVisitorConvoInfo(models.Model):
    room_slug = models.CharField(max_length=25)
    cso_email = models.CharField(max_length=60, verbose_name='Customer Support Officer Email')
    is_resolved = models.BooleanField(default=False)
    is_connected = models.BooleanField(verbose_name='Is CSO connected?', default=False)
    created_at = models.DateTimeField(verbose_name="Conversation created at", auto_now=True)

    class Meta:
        verbose_name_plural = "CSO Visitor Conversation Information"
