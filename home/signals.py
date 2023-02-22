from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerSupportRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=CustomerSupportRequest)
def customer_support_request_signal(sender, instance, created, **kwargs):
    if created:
        print("[from 'customer_support_request_signal*()' func]New customer support request is created!")
        data = CustomerSupportRequest.get_customer_support_reqs()
        print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")

        # Broadcast the "data" into the "CSODashboardConsumer" consumer channel-group
        # Solution: https://stackoverflow.com/a/7811582
        # [Explanation] Create a method in the consumer-class which will be responsible 
        # for sending the payload to each individual cso-channel's frontend wbSocket 
        # through "CSODashboardConsumer".
        channel_layer = get_channel_layer()
        # TODO: This signal will be custom-made later, logic will be implemented here to decide in which cso-support-dashboard-channel the request will be sent to.
        cso_email = "tanjim.ashraf@doer.com.bd"
        room_name_normalized="".join(ch for ch in cso_email if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        async_to_sync(channel_layer.group_send)(
            f'chat_dashboard_{room_name_normalized}',
            {
                'type': 'new_support_req', 
                'new_support_request': data
            }
        )
