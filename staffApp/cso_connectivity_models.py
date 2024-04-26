from django.db import models
from home.models import CustomerSupportRequest


class CSOOnline(models.Model):
    cso_email = models.CharField(verbose_name='HDO email', max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    is_active = models.BooleanField(verbose_name='HDO active', default=True)
    joined_at = models.DateTimeField(verbose_name="Joined at", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last activity", auto_now=True)
    user_organization = models.CharField(verbose_name='Organization', max_length=100, blank=True, null=True)
    location = models.CharField(verbose_name='Location', max_length=100, blank=True, null=True)
    district = models.CharField(verbose_name='District', max_length=100, blank=True, null=True)
    division = models.CharField(verbose_name='Division', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "HDO Online (inside System)"

    @staticmethod
    def customer_support_request_counter(hdo_email):
        return len(CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=hdo_email))

    @staticmethod
    def cso_filtration(
        instances:object,
        user_organization:str,
        location:str,
        district:str,
        division:str,
    ):
        filtered_instances = dict() # MIGHT CONTAIN REDUNDANCY
        for i in instances:
            if (i['user_organization'] == user_organization) and \
                    (i['location'] == location):
                filtered_instances[f'{i["cso_email"]}'] = i

            if i['user_organization'] == user_organization:
                filtered_instances[f'{i["cso_email"]}'] = i

            if i['location'] == location:
                filtered_instances[f'{i["cso_email"]}'] = i

            if i['district'] == district:
                filtered_instances[f'{i["cso_email"]}'] = i

            if i['division'] == division:
                filtered_instances[f'{i["cso_email"]}'] = i
        return filtered_instances

    @staticmethod
    def get_cso_online(
            user_organization, 
            location, 
            district, 
            division):
        # If any of the param is None, then list out all the values excluding user_organization, location, district, division
        if user_organization is None \
            or location is None \
            or district is None \
            or division is None:
            instances = list(CSOOnline.objects.values('cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update', 'user_organization', 'location', 'district', 'division'))
            return instances
        else:
            instances = list(CSOOnline.objects.values(
                'cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update',
                'user_organization', 'location', 'district', 'division'
            ))
            # instances = CSOOnline.cso_filtration(
            #     user_organization=user_organization,
            #     location=location,
            #     district=district,
            #     division=division,
            #     instances=instances
            # )
            return instances

    @staticmethod
    def get_active_cso(
            user_organization=None, 
            location=None, 
            district=None, 
            division=None,
            loc_support_confirmation=False,
            gen_support_confirmation=False):
        instances = CSOOnline.get_cso_online(
            user_organization=user_organization,
            location=location,
            district=district,
            division=division)
        active_cso = []
        if user_organization is None \
            or location is None \
            or district is None \
            or division is None:
            for i in instances:
                if i['is_active']:
                    active_cso.append(i)

            if gen_support_confirmation:
                clear_flag = True
                for ac in active_cso:
                    if CSOOnline.customer_support_request_counter(hdo_email=ac['cso_email']) < 5:
                        clear_flag = False
                if clear_flag:
                    active_cso.clear()

            return active_cso
        else:
            # filtered_cso_list = [i[1] for i in instances.items()]
            
            for i in instances:
                if i.get('is_active'):
                    active_cso.append(i)

            # for i in filtered_cso_list:
            #     if i['is_active']:
            #         active_cso.append(i)
            
            if len(active_cso) == 0:
                return CSOOnline.get_active_cso(gen_support_confirmation=True)

            if loc_support_confirmation:
                recall_flag = True
                for ac in active_cso:
                    if CSOOnline.customer_support_request_counter(hdo_email=ac['cso_email']) < 5:
                        recall_flag = False
                if recall_flag:
                    return CSOOnline.get_active_cso(gen_support_confirmation=True)

            return active_cso


class CSOConnectedChannels(models.Model):
    cso_email = models.CharField(verbose_name='HDO email', max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    channel_value = models.CharField(max_length=74)

    class Meta:
        verbose_name_plural = "HDO Channels (inside System)"
