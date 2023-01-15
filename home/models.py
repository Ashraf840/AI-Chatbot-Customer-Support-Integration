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
    created_at = models.DateTimeField(verbose_name="Created at", auto_now=True)

    class Meta:
        verbose_name_plural = "Customer Support Request"

    @staticmethod
    def get_customer_support_reqs():
        # instances = CustomerSupportRequest.objects.all()
        instances = list(CustomerSupportRequest.objects.values('client_ip', 'room_slug'))   # Solution: https://stackoverflow.com/a/7811582
        # data = [i for i in instances]
        # data = instances
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
