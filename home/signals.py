from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerSupportRequest, CSOVisitorConvoInfo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from staffApp.cso_connectivity_models import CSOOnline
from home.utils.messageRequestDistributionProtocol import NewCustomerDistribution


@receiver(post_save, sender=CustomerSupportRequest)
def customer_support_request_signal(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    # On Create
    if created:
        print("[from 'customer_support_request_signal*()' func]New customer support request is created!")
        
        print('\n'*2)
        print('#'*50)
        # TODO: Get all the total active CSOs in the system.
        active_cso = CSOOnline.get_active_cso()
        # print(f'Active cso: {active_cso}')
        # total_active_cso = len(active_cso)
        # TODO: Get all the message_requests where the cso_email is not null
        total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso()
        # cso_user_chat_info = CSOVisitorConvoInfo.get_unresolved_msg()
        # room_tuple = tuple([r['room_slug'] for r in cso_user_chat_info])
        # unresolved_total_msg = []
        # for tm in total_msg:
        #     if tm['room_slug'] in room_tuple:
        #         unresolved_total_msg.append(tm)
        
        # total_msg = unresolved_total_msg

        # print(f'Total msg: {total_msg}')
        # keys = ['cso', 'num_of_chats']
        # print(total_msg)
        # for msg in total_msg:
        #     print(msg['assigned_cso'])

        new_dict= [{'cso': msg['assigned_cso'], 'created_at': msg['created_at']} for msg in total_msg]
        for dt in new_dict:
            print(dt)

        msg_req = []
        for msg in total_msg:
            msg_req.append(msg['assigned_cso'])
        msg_req_set = set(msg_req)
        msg_count = []
        msg_req_list = list(msg_req_set)
        for i in msg_req_list:
            msg_count.append(msg_req.count(i))

        cso_num_of_chats = zip(msg_req_list, msg_count)
        cso_num_of_chats_list = []
        for i in cso_num_of_chats:
            cso_num_of_chats_list.append(i)

        for cnocl in cso_num_of_chats_list:
            print(cnocl)


        data_1, data_2 = new_dict, cso_num_of_chats_list
        data_1_processed = []
        for entry in data_1:
            data_1_processed.append({
                'cso': entry['cso'],
                'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            })
        # print('data_1_processed \n',data_1_processed)
        # Create dictionary mapping CSOs to number of chats from data_2
        cso_to_chats = dict(data_2)

        # print('CSO to chats \n', cso_to_chats, '\n')
        # Combine data_1 and data_2 to create final list
        data = []
        ids_processed = set()
        # print('ids_processed',ids_processed,'\n')

        for entry in data_1_processed:
            cso = entry['cso']
            num_of_chats = cso_to_chats.get(cso, 0)
            if cso not in ids_processed:
                ids_processed.add(cso)
                data.append({
                    'time': entry['created_at'],
                    'id': cso,
                    'num_of_chats': num_of_chats
                })

        # for d in data:
        #     print(d)


        # msg_distribution = NewCustomerDistribution(amt_of_members=5, max_amt_of_chats_per_member=5, cso_id_chatamt_timestamp=data)
        # next_cso = msg_distribution.add_new_chat()
        # print(f'next_cso: {next_cso}')

        # Broadcast the "data" into the "CSODashboardConsumer" consumer channel-group
        # Solution: https://stackoverflow.com/a/7811582
        # [Explanation] Create a method in the consumer-class which will be responsible 
        # for sending the payload to each individual cso-channel's frontend wbSocket 
        # through "CSODashboardConsumer".
        # channel_layer = get_channel_layer()   # MOVED TO THE TOP

        # TODO: This signal will be custom-made later, logic will be implemented here to decide in which cso-support-dashboard-channel the request will be sent to.
        cso_email = "tanjim.ashraf@doer.com.bd"
        # cso_email = "tanjim.ashraf.doer.bp@gmail.com"
        next_cso = cso_email    # COMMENT IT
        # instance.assigned_cso = cso_email
        instance.assigned_cso = next_cso      # OK
        instance.save()

        # Get all the message reqs of the individual CSO
        data = CustomerSupportRequest.get_customer_support_reqs()
        # print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")
        result = []

        for i in data:
            if i['assigned_cso'] == next_cso:
                # print(i)
                result.append(i)
        # print(f'Result (based of assigned CSO: {result})')
        print('#'*50)
        print('\n'*2)
        
        room_name_normalized="".join(ch for ch in next_cso if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        async_to_sync(channel_layer.group_send)(
            f'chat_dashboard_{room_name_normalized}',
            {
                'type': 'new_support_req', 
                'new_support_request': result,
            }
        )

    # On update
    if not created:
        # print('\n'*3)
        # print('+'*50)
        # print(f'Update the customer support request! {instance.is_resolved}')

        instance_room_slug = instance.room_slug
        instance_resolved = instance.is_resolved
        instance_cso_email = instance.assigned_cso
        room_name_normalized="".join(ch for ch in instance_cso_email if ch.isalnum())
        async_to_sync(channel_layer.group_send)(
            f'chat_dashboard_{room_name_normalized}',
            {
                'type': 'old_support_req_resolved', 
                'instance_room_slug': instance_room_slug,
                'instance_resolved': instance_resolved,
            }
        )
        # print('+'*50)
        # print('\n'*3)   