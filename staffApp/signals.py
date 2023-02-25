from django.db.models.signals import post_save
from django.dispatch import receiver
from .cso_connectivity_models import CSOOnline
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CSOOnline)
def cso_online_signal(sender, instance, created, **kwargs):
    # print(f"Instance type: {type(instance)}")
    # record = instance
    if created:
        print("[from 'cso_online_signal*()' func] New online activity of a CSO created!")
        print(f"New instance: {instance}")
        print(f"CSO ID: {instance.pk}")
        print(f"New instance email: {instance.cso_email}")
        print(f"New instance room-slug: {instance.room_slug}")

        # Broadcast the "data" into the "CSOOnlineConnectivityConsumer" consumer channel-group
        # [Explanation] Create a method in the consumer-class which will be responsible 
        # for sending the payload to each individual cso-channel's frontend wbSocket 
        # through "CSODashboardConsumer".
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'cso_online_connectivity_dashboard',
            {
                'type': 'cso_online_connectivity', 
                'instance_id': instance.pk,
                'connectivity_report_email': instance.cso_email,
                'connectivity_report_room_slug': instance.room_slug,
                'connectivity_report_online': instance.is_active,
                'connectivity_report_joined_at': str(instance.joined_at),
                'connectivity_report_last_update': str(instance.last_update),
                'connectivity_status': 'new',
            }
        )
    else:
        print("[from 'cso_online_signal*()' func] Old record of online activity of a CSO is modified!")
        print(f"Old instance: {instance}")
        print(f"CSO ID: {instance.pk}")
        print(f"New instance email: {instance.cso_email}")
        print(f"New instance room-slug: {instance.room_slug}")

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'cso_online_connectivity_dashboard',
            {
                'type': 'cso_online_connectivity', 
                'instance_id': instance.pk,
                'connectivity_report_email': instance.cso_email,
                'connectivity_report_room_slug': instance.room_slug,
                'connectivity_report_online': instance.is_active,
                'connectivity_report_joined_at': str(instance.joined_at),
                'connectivity_report_last_update': str(instance.last_update),
                'connectivity_status': 'old',
            }
        )
