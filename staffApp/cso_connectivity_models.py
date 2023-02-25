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

    @staticmethod
    def get_cso_online():
        """
        This method is used to return all the records of currently online/offline CSO.
        """
        instances = list(CSOOnline.objects.values('cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update'))   # Solution: https://stackoverflow.com/a/7811582
        return instances

    @staticmethod
    def get_active_cso():
        """
        This method is used to return all the records of currently online CSO. This approach is taken because the database of this project is used as mongodb, 
        since mongodb is not supported native django-filtering.
        """
        instances = CSOOnline.get_cso_online()
        active_cso = []
        for i in instances:
            if i['is_active']:
                active_cso.append(i)
        return active_cso


class CSOConnectedChannels(models.Model):
    cso_email = models.CharField(max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    channel_value = models.CharField(max_length=74)

    class Meta:
        verbose_name_plural = "CSO Channels (inside System)"
