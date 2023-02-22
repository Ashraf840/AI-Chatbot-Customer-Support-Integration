from django.db import models


# NB: All the models of this file are registered in 'admins.py' file of the battery

class CSOOnline(models.Model):
    cso_email = models.CharField(max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    is_active = models.BooleanField(verbose_name='CSO active', default=True)
    joined_at = models.DateTimeField(verbose_name="Joined at", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last activity", auto_now=True)

    class Meta:
        verbose_name_plural = "CSO Online (inside System)"


class CSOConnectedChannels(models.Model):
    cso_email = models.CharField(max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    channel_value = models.CharField(max_length=74)

    class Meta:
        verbose_name_plural = "CSO Channels (inside System)"
