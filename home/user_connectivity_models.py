from django.db import models


# NB: All the models of this file are registered in 'admins.py' file of the battery

class ChatSupportUserOnline(models.Model):
    cso_email = models.CharField(max_length=60, blank=True, null=True)
    visitor_session_uuid = models.CharField(max_length=36, blank=True, null=True)
    room_slug = models.CharField(max_length=25)
    is_active = models.BooleanField(verbose_name='User active', default=True)
    joined_at = models.DateTimeField(verbose_name="Joined at", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last activity", auto_now=True)

    class Meta:
        verbose_name_plural = "Customer Support (Chat) CSO-Visitor Chat Online"


class ChatSupportUserConnectedChannels(models.Model):
    cso_email = models.CharField(max_length=60, blank=True, null=True)
    visitor_session_uuid = models.CharField(max_length=36, blank=True, null=True)
    room_slug = models.CharField(max_length=25)
    channel_value = models.CharField(max_length=74)

    class Meta:
        verbose_name_plural = "Customer Support (Chat) CSO-Visitor Channels"
