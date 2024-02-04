from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomerSupportRequest, CSOVisitorConvoInfo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from staffApp.cso_connectivity_models import CSOOnline
from authenticationApp.utils.userDetail import UserDetail
from .utils.hdo_filtration import LocationBasedActiveHDOFiltration
from .utils.msg_amount_checker import MessageAmountChecker


@receiver(post_save, sender=CustomerSupportRequest)
def customer_support_request_signal_post_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if created:
        user_detail = UserDetail(user_email=instance.registered_user_email)
        user_profile = user_detail.user_profile_detail(instance.registered_user_email)
        active_cso = CSOOnline.get_active_cso(
            user_organization=user_profile.user_organization,
            location=user_profile.location,
            district=user_profile.district,
            division=user_profile.division
        )

        if len(active_cso) == 1:
                instance.assigned_cso = active_cso[0]['cso_email']
                instance.save()     

        if len(active_cso) > 1:
            location_based_active_hdo_filtration = LocationBasedActiveHDOFiltration(active_cso=active_cso, user_profile=user_profile)
            message_amount_checker = MessageAmountChecker(instance=instance)
            filtered_hdo = []
            filtered_hdo = location_based_active_hdo_filtration.exact_match()
            
            if len(filtered_hdo) == 1:
                result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                if not result:
                    filtered_hdo.clear()

            if len(filtered_hdo) > 1:
                result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                if not result:
                    filtered_hdo.clear()

            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.org_loc_match()
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.org_match()
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.loc_match()
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.dist_match()
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()


            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.div_match()
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()


            if len(filtered_hdo) == 0:
                filtered_hdo = location_based_active_hdo_filtration.gen_match()

                no_loc_hdo, diff_hdo = [], []
                
                for fhd in filtered_hdo:
                    if fhd['user_organization'] is None \
                    and fhd['location'] is None \
                    and fhd['district'] is None \
                    and fhd['division'] is None:
                        no_loc_hdo.append(fhd)
                    else:
                        diff_hdo.append(fhd)
                
                if no_loc_hdo:
                    if len(no_loc_hdo) == 1:
                        result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=no_loc_hdo)
                        if not result:
                            no_loc_hdo.clear()

                    if len(no_loc_hdo) > 1:
                            result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=no_loc_hdo)
                            if not result:
                                no_loc_hdo.clear()
                
                if not no_loc_hdo and diff_hdo:
                    if len(diff_hdo) == 1:
                        result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=diff_hdo)
                        if not result:
                            diff_hdo.clear()

                    if len(diff_hdo) > 1:
                        result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=diff_hdo)
                        if not result:
                            diff_hdo.clear()




    if not created:
        instance_room_slug = instance.room_slug
        instance_resolved = instance.is_resolved
        instance_dismissed = instance.is_dismissed
        instance_detached = instance.is_detached
        instance_assigned_cso = instance.assigned_cso
        room_name_normalized="".join(ch for ch in instance_assigned_cso if ch.isalnum())

        if not instance_detached and not instance_dismissed and not instance_resolved:
            data = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=instance_assigned_cso) 

            for d in data:
                del d['created_at']
            
            async_to_sync(channel_layer.group_send)(
                f'chat_dashboard_{room_name_normalized}',
                {
                    'type': 'new_support_req', 
                    'new_support_request': data,
                }
            )
        else:
            result_r_d = "Resolve Socket" if instance_resolved else "Dismiss Socket" if instance_dismissed else True
            data = CustomerSupportRequest.get_customer_support_reqs()
            total_current_reqs = len(data)

            if instance_resolved:
                async_to_sync(channel_layer.group_send)(
                    f'chat_dashboard_{room_name_normalized}',
                    {
                        'type': 'old_support_req_resolved', 
                        'instance_room_slug': instance_room_slug,
                        'instance_resolved': instance_resolved,
                        'total_current_reqs': total_current_reqs,
                    }
                )
            
            if instance_dismissed:
                async_to_sync(channel_layer.group_send)(
                    f'chat_dashboard_{room_name_normalized}',
                    {
                        'type': 'old_support_req_dismissed', 
                        'instance_room_slug': instance_room_slug,
                        'instance_dismissed': instance_dismissed,
                        'total_current_reqs': total_current_reqs,
                    }
                )





@receiver(post_delete, sender=CustomerSupportRequest)
def customer_support_request_signal_post_delete(sender, instance, **kwargs):
    try:
        cso_user_chat_info = CSOVisitorConvoInfo.objects.get(room_slug=instance.room_slug)
        cso_user_chat_info.is_cleared = True
        cso_user_chat_info.is_connected = False
        cso_user_chat_info.save()
        channel_layer = get_channel_layer()
        if (cso_user_chat_info.is_cancelled):
            async_to_sync(channel_layer.group_send)(
                f'chat_{cso_user_chat_info.room_slug}',
                {
                    'type': 'support_request_cleared', 
                    'CSOVisitorConvoInfo_isCancelled': True,
                }
            )
        data = CustomerSupportRequest.get_unresolved_customer_support_reqs()
        total_current_reqs_after_convo_cancelled = len(data)
        room_name_normalized="".join(ch for ch in instance.assigned_cso if ch.isalnum())
        async_to_sync(channel_layer.group_send)(
            f'chat_dashboard_{room_name_normalized}',
            {
                'type': 'support_req_chat_convo_cancelled', 
                'instance_room_slug': instance.room_slug,
                'total_current_reqs_after_convo_cancelled': total_current_reqs_after_convo_cancelled,
            }
        )
    except:
        print("Cannot find any such record in 'CSOVisitorConvoInfo' model")




"""
@receiver(post_delete, sender=CustomerSupportRequest)
def customer_support_request_signal_post_delete(sender, instance, **kwargs):
    try:
        cso_user_chat_info = CSOVisitorConvoInfo.objects.get(room_slug=instance.room_slug)
        cso_user_chat_info.is_cleared = True
        cso_user_chat_info.is_connected = False
        cso_user_chat_info.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{cso_user_chat_info.room_slug}',
            {
                'type': 'support_request_cleared', 
            }
        )
        data = CustomerSupportRequest.get_unresolved_customer_support_reqs()
        total_current_reqs_after_convo_cancelled = len(data)
        room_name_normalized="".join(ch for ch in instance.assigned_cso if ch.isalnum())
        async_to_sync(channel_layer.group_send)(
            f'chat_dashboard_{room_name_normalized}',
            {
                'type': 'support_req_chat_convo_cancelled', 
                'instance_room_slug': instance.room_slug,
                'total_current_reqs_after_convo_cancelled': total_current_reqs_after_convo_cancelled,
            }
        )
    except:
        print("Cannot find any such record in 'CSOVisitorConvoInfo' model")


"""
