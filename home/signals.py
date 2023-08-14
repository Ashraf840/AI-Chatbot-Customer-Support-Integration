from django.db.models.signals import post_save, post_delete#, pre_delete
from django.dispatch import receiver
from .models import CustomerSupportRequest, CSOVisitorConvoInfo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from staffApp.cso_connectivity_models import CSOOnline
# from home.utils.messageRequestDistributionProtocol import NewCustomerDistribution
# import random
from authenticationApp.utils.userDetail import UserDetail
from .utils.hdo_filtration import LocationBasedActiveHDOFiltration
from .utils.msg_amount_checker import MessageAmountChecker


@receiver(post_save, sender=CustomerSupportRequest)
def customer_support_request_signal_post_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    # On Create
    if created:
        print('\n'*2)
        print('#'*50)
        print("[from 'customer_support_request_signal_post_save*()' func]New customer support request is created!")
        
        # Get the user-profile-detail thru "CustomerSupportRequest" model's "registered_user_email" [*newly added to this model for this purpose]
        user_detail = UserDetail(user_email=instance.registered_user_email)
        user_profile = user_detail.user_profile_detail()
        # {user_profile.user_organization, user_profile.location, user_profile.district, user_profile.division}
        # Then pass that user's {org, loc, dist, div} into the param of "CSOOnline.get_active_cso()" to make more precise filtration of active-csos.

        # TODO: Get all the total active CSOs in the system.
        # active_cso = CSOOnline.get_active_cso()
        active_cso = CSOOnline.get_active_cso(
            user_organization=user_profile.user_organization, 
            location=user_profile.location, 
            district=user_profile.district, 
            division=user_profile.division
        )
        # print(f'Active cso: {active_cso}')
        # total_active_cso = len(active_cso)


        # Single Active CSO (HDO) currently in the system
        if len(active_cso) == 1:                
                instance.assigned_cso = active_cso[0]['cso_email']
                instance.save()     # will got to update-code-block


        if len(active_cso) > 1:
            location_based_active_hdo_filtration = LocationBasedActiveHDOFiltration(active_cso=active_cso, user_profile=user_profile)
            message_amount_checker = MessageAmountChecker(instance=instance)

            # There suppose to be a function, where we pass the filled/empty "filtered_hdo[]" along with "location_based_active_hdo_filtration" obj

            filtered_hdo = []
            
            # [01]
            filtered_hdo = location_based_active_hdo_filtration.exact_match()
            # if {org, loc, dist, div} matched
            # for ac in active_cso:
                # [04] - nodup "exact_match"
                # if ac["user_organization"] == user_profile.user_organization and ac["location"] == user_profile.location and ac["district"] == user_profile.district and ac["division"] == user_profile.division:
                #     # print(ac["user_organization"], ac["location"], ac["district"], ac["division"])
                #     filtered_hdo.append(ac)
            if len(filtered_hdo) == 1:
                # Check if the HDO is handling more/less than 5 reqs; 
                result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                if not result:
                    filtered_hdo.clear()

            if len(filtered_hdo) > 1:
                # Check which HDO is handling least amount of msg
                result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                if not result:
                    filtered_hdo.clear()

            
            # [02]
            # if previously doesn't found any elem for "filtered_hdo", then if {org, loc} matched
            if len(filtered_hdo) == 0:
                # [04] - nodup "org_loc_match"
                filtered_hdo = location_based_active_hdo_filtration.org_loc_match()
                # for ac in active_cso:
                #     if ac["user_organization"] == user_profile.user_organization and ac["location"] == user_profile.location:
                #         filtered_hdo.append(ac)
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()
            

            # [03]
            # if previously doesn't found any elem for "filtered_hdo", then if only {org} matched
            if len(filtered_hdo) == 0:
                # [04] - nodup "org_match"
                filtered_hdo = location_based_active_hdo_filtration.org_match()
                # for ac in active_cso:
                #     if ac["user_organization"] == user_profile.user_organization:
                #         filtered_hdo.append(ac)
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()
            

            # [04]
            # if previously doesn't found any elem for "filtered_hdo", then if only {loc} matched
            if len(filtered_hdo) == 0:
                # [07] - nodup "loc_match"
                filtered_hdo = location_based_active_hdo_filtration.loc_match()
                # for ac in active_cso:
                #     if ac["location"] == user_profile.location:
                #         filtered_hdo.append(ac)
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()
            

            # [05]
            # if previously doesn't found any elem for "filtered_hdo", then if only {dist} matched
            if len(filtered_hdo) == 0:
                # [09] - nodup "dist_match"
                filtered_hdo = location_based_active_hdo_filtration.dist_match()
                # for ac in active_cso:
                #     if ac["district"] == user_profile.district:
                #         filtered_hdo.append(ac)
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()
            

            # [06]
            # if previously doesn't found any elem for "filtered_hdo", then if only {div} matched
            if len(filtered_hdo) == 0:
                # [14] - nodup "div_match"
                filtered_hdo = location_based_active_hdo_filtration.div_match()
                # for ac in active_cso:
                #     if ac["division"] == user_profile.division:
                #         filtered_hdo.append(ac)
                if len(filtered_hdo) == 1:
                    result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()

                if len(filtered_hdo) > 1:
                    result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                    if not result:
                        filtered_hdo.clear()
            
            
            # [07]
            # if previously doesn't found any elem for "filtered_hdo", then get all the active HDOs regardless of their {org, loc, dist, div}
            if len(filtered_hdo) == 0:
                # [30] - **nodup  get all active HDOs "gen_match"
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

                # general_cso = CSOOnline.get_active_cso()
                # for ac in general_cso:
                #     filtered_hdo.append(ac)

                # [First Priority] try to validate if there is any no_loc_hod w/ active-status who has less than 5 chats to handle the next support-request.
                if no_loc_hdo:
                    if len(no_loc_hdo) == 1:
                        result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=no_loc_hdo)
                        if not result:
                            no_loc_hdo.clear()
                            # TODO: **(if necessary) FURTHER ERROR HANDLING: Redirect the user to homepage with a msg-popup, that a representative will contact him/her soon

                    if len(no_loc_hdo) > 1:
                        result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=no_loc_hdo)
                        if not result:
                            no_loc_hdo.clear()
                            # TODO: **(if necessary) FURTHER ERROR HANDLING: Redirect the user to homepage with a msg-popup, that a representative will contact him/her soon
                
                # [Second Priority] if there is no such "no_loc_hdo" who can handle this next chat, then randomly send the next msg-request to an active HDO regardless of his/her {org, loc, dist, div}, even if some of location-based-set of HDO is empty.
                if not no_loc_hdo and diff_hdo:
                    if len(diff_hdo) == 1:
                        result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=diff_hdo)
                        if not result:
                            diff_hdo.clear()
                            # TODO: **(if necessary) FURTHER ERROR HANDLING: Redirect the user to homepage with a msg-popup, that a representative will contact him/her soon

                    if len(diff_hdo) > 1:
                        result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=diff_hdo)
                        if not result:
                            diff_hdo.clear()
                            # TODO: **(if necessary) FURTHER ERROR HANDLING: Redirect the user to homepage with a msg-popup, that a representative will contact him/her soon


                # []DEPRECATED CODE ---------------------------------------
                # filtered_hdo = location_based_active_hdo_filtration.gen_match()
 
                # if len(filtered_hdo) == 1:
                #     result = message_amount_checker.singular_msg_amount_checker(filtered_hdo=filtered_hdo)
                #     if not result:
                #         filtered_hdo.clear()

                # if len(filtered_hdo) > 1:
                #     result = message_amount_checker.multiple_msg_amount_checker(filtered_hdo=filtered_hdo)
                #     if not result:
                #         filtered_hdo.clear()
                # ---------------------------------------
            # CODE HERE [DONE ABOVE] <------------------------------------------------
            

            
            
            
            
            
            
            
            
            # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # # filtered_hdo_check = filtered_hdo

            # # if "filtered_hdo" contain single/multiple elem
            # if len(filtered_hdo) == 1:
            #     # Check if that HDO is handling more than or equal to 5 msg
            #     handling_msg_amount = len(CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=filtered_hdo[0]['cso_email']))
            #     if handling_msg_amount >= 5:
            #         # Make filtration again
            #         filtered_hdo.clear()
            #         filtered_hdo = location_based_active_hdo_filtration.org_loc_match()

            #         if len(filtered_hdo) == 1:
            #             filtered_hdo.clear()
            #             filtered_hdo = location_based_active_hdo_filtration.org_match()
            #         if len(filtered_hdo) > 1:
            #             pass

            #         pass
            #     else:
            #         # That HDO is not handling more than 5 msg
            #         instance.assigned_cso = filtered_hdo[0]['cso_email']
            #         instance.save()
            #         pass
            #     pass
            
            # if len(filtered_hdo) > 1:
            #     # Check which HDO is handling least amount of msg
            #     pass
            # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++









        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # # TODO: Get all the message_requests where the cso_email is not null
        # # total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso()
        # total_msg = CustomerSupportRequest.get_customer_support_reqs()      # [used for validating if the msg-pool is currently empty/not in the system] get in general all msg-req which are not detached yet/ "is_detached=False"
        
        
        # # cso_user_chat_info = CSOVisitorConvoInfo.get_unresolved_msg()
        # # room_tuple = tuple([r['room_slug'] for r in cso_user_chat_info])
        # # unresolved_total_msg = []
        # # for tm in total_msg:
        # #     if tm['room_slug'] in room_tuple:
        # #         unresolved_total_msg.append(tm)
        
        # # total_msg = unresolved_total_msg
        # # unresolved_total_msg = total_msg

        # print(f'Total msg: {total_msg}')
        # print(f'Total msg-length: {len(total_msg)}')
        # # keys = ['cso', 'num_of_chats']
        # # print(total_msg)
        # # for msg in total_msg:
        # #     print(msg['assigned_cso'])
        
        
        
        # # return True

        # # TODO: Check if 'total_msg' list is empty  [MESSAGE-POOL IS EMPTY]
        # # NB:  ***MSG-POOL IS NOT EMPTY AT THIS POINT SINCE THE CUST-SPPRT-REQ IS CREATED & THEN DJ COMES TO THIS FOLLOWING CODE BLOCK
        # # -------------------------------------------------------------------------------------------------------------------
        # if len(total_msg) == 0:
        #     print("Msg-pool is empty!")



        #     # ---------------------------------------------------------------------------------------------------------------
        #     # TODO: Check if length of 'active_cso' is more than 1.
        #     if len(active_cso) > 1:
        #         active_cso_emails = [ac['cso_email'] for ac in active_cso]
        #         print(f'Only active cso emails: {active_cso_emails}')
        #         selected_active_cso_email = random.choice(active_cso_emails)    # randomly select a CSO among the active-CSOs (......)
        #         print(f'Selected active cso emails: {selected_active_cso_email}')
        #         # TODO: Save the randomly selected cso-email into the instance's 'assigned_cso' field
        #         next_cso = selected_active_cso_email    # COMMENT IT
        #         instance.assigned_cso = next_cso      # OK
        #         instance.save()
        #         room_name_normalized="".join(ch for ch in next_cso if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        #         # Get all the message reqs of the individual CSO
        #         data = CustomerSupportRequest.get_customer_support_reqs()
        #         # print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")
        #         result = []
        #         for i in data:
        #             if i['assigned_cso'] == next_cso:
        #                 # print(i)
        #                 result.append(i)


        #         # [01]
        #         async_to_sync(channel_layer.group_send)(
        #             f'chat_dashboard_{room_name_normalized}',
        #             {
        #                 'type': 'new_support_req', 
        #                 'new_support_request': result,
        #             }
        #         )

        #     # TODO: Check if length of 'active_cso' is equal to 1.
        #     if len(active_cso) == 1:
        #         next_cso = active_cso[0]['cso_email']    # COMMENT IT
        #         instance.assigned_cso = next_cso      # OK
        #         instance.save()
        #         room_name_normalized="".join(ch for ch in next_cso if ch.isalnum())
        #         # Get all the message reqs of the individual CSO
        #         data = CustomerSupportRequest.get_customer_support_reqs()       # TODO: get only the NEW SUPPORT-REQ where the CSO is not assigned & "is_detached=False"
        #         # print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")
        #         result = []
        #         for i in data:
        #             if i['assigned_cso'] == next_cso:
        #                 # print(i)
        #                 result.append(i)

        #         # [02]
        #         async_to_sync(channel_layer.group_send)(
        #             f'chat_dashboard_{room_name_normalized}',
        #             {
        #                 'type': 'new_support_req', 
        #                 'new_support_request': result,
        #             }
        #         )

        #     # ---------------------------------------------------------------------------------------------------------------





        # # -------------------------------------------------------------------------------------------------------------------
        # # Message-pool is not empty
        # else:
        #     # print("Msg-pool is not empty!")
        #     # new_dict= [{'cso': msg['assigned_cso'], 'created_at': msg['created_at']} for msg in total_msg]
        #     # print(f'total active cso (handling chats - dict): {len(new_dict)}')

        #     """ [NOT USING HERE]
        #     active_cso_list = [x['cso_email'] for x in active_cso]
        #     cso_email_total_msg_list = [x['assigned_cso'] for x in total_msg]
        #     fresh_cso_no_msg = list(set(active_cso_list).symmetric_difference(set(cso_email_total_msg_list)))
        #     """
        #     # Find all the active (online) CSOs who are not currently handling any requests, randomly distribute messages until no active CSO left with 0 messages.
        #     # If there is no fresh CSO left handling any msg-reqs, Only then pass through Zubair vai's algo.
            
            
        #     if len(active_cso) == 1:                
        #         instance.assigned_cso = active_cso[0]['cso_email']
        #         instance.save()     # will got to update-code-block


        #     if len(active_cso) > 1:
        #         filtered_hdo = []
                
        #         # if {org, loc, dist, div} matched
        #         for ac in active_cso:
        #             # [04] - nodup "exact_match"
        #             if ac["user_organization"] == user_profile.user_organization and ac["location"] == user_profile.location and ac["district"] == user_profile.district and ac["division"] == user_profile.division:
        #                 # print(ac["user_organization"], ac["location"], ac["district"], ac["division"])
        #                 filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then if {org, loc} matched
        #         if len(filtered_hdo) == 0:
        #             # [04] - nodup "org_loc_match"
        #             for ac in active_cso:
        #                 if ac["user_organization"] == user_profile.user_organization and ac["location"] == user_profile.location:
        #                     filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then if only {org} matched
        #         if len(filtered_hdo) == 0:
        #             # [04] - nodup "org_match"
        #             for ac in active_cso:
        #                 if ac["user_organization"] == user_profile.user_organization:
        #                     filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then if only {loc} matched
        #         if len(filtered_hdo) == 0:
        #             # [07] - nodup "loc_match"
        #             for ac in active_cso:
        #                 if ac["location"] == user_profile.location:
        #                     filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then if only {dist} matched
        #         if len(filtered_hdo) == 0:
        #             # [09] - nodup "dist_match"
        #             for ac in active_cso:
        #                 if ac["district"] == user_profile.district:
        #                     filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then if only {div} matched
        #         if len(filtered_hdo) == 0:
        #             # [14] - nodup "div_match"
        #             for ac in active_cso:
        #                 if ac["division"] == user_profile.division:
        #                     filtered_hdo.append(ac)
                
        #         # if previously doesn't found any elem for "filtered_hdo", then get all the active HDOs regardless of their {org, loc, dist, div}
        #         if len(filtered_hdo) == 0:
        #             # [30] - **nodup  get all active HDOs "gen_match"
        #             general_cso = CSOOnline.get_active_cso()
        #             for ac in general_cso:
        #                 filtered_hdo.append(ac)
                








        #         # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #         # [ U N C O M M E N T ]
        #         active_cso_list = [x['cso_email'] for x in filtered_hdo]
        #         total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso()
        #         cso_email_total_msg_list = [x['assigned_cso'] for x in total_msg]
        #         fresh_cso_no_msg = list(set(active_cso_list).symmetric_difference(set(cso_email_total_msg_list)))

        #         next_cso = None
        #         if len(fresh_cso_no_msg) >= 1:
        #             selected_active_cso_email = random.choice(fresh_cso_no_msg)
        #             next_cso = selected_active_cso_email    # COMMENT IT
        #             instance.assigned_cso = next_cso      # OK
        #             instance.save()
        #         else:
        #             new_dict= [{'cso': msg['assigned_cso'], 'created_at': msg['created_at']} for msg in total_msg]
        #             # ############################################################################
        #             # for dt in new_dict:
        #             #     print(dt)

        #             msg_req = []
        #             for msg in total_msg:
        #                 msg_req.append(msg['assigned_cso'])
        #             msg_req_set = set(msg_req)
        #             msg_count = []
        #             msg_req_list = list(msg_req_set)
        #             for i in msg_req_list:
        #                 msg_count.append(msg_req.count(i))

        #             cso_num_of_chats = zip(msg_req_list, msg_count)
        #             cso_num_of_chats_list = []
        #             for i in cso_num_of_chats:
        #                 cso_num_of_chats_list.append(i)

        #             for cnocl in cso_num_of_chats_list:
        #                 print(cnocl)

        #             data_1, data_2 = new_dict, cso_num_of_chats_list
        #             data_1_processed = []
        #             for entry in data_1:
        #                 data_1_processed.append({
        #                     'cso': entry['cso'],
        #                     'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        #                 })
        #             # print('data_1_processed \n',data_1_processed)
        #             # Create dictionary mapping CSOs to number of chats from data_2
        #             cso_to_chats = dict(data_2)

        #             # print('CSO to chats \n', cso_to_chats, '\n')
        #             # Combine data_1 and data_2 to create final list
        #             data = []
        #             ids_processed = set()
        #             # print('ids_processed',ids_processed,'\n')

        #             for entry in data_1_processed:
        #                 cso = entry['cso']
        #                 num_of_chats = cso_to_chats.get(cso, 0)
        #                 if cso not in ids_processed:
        #                     ids_processed.add(cso)
        #                     data.append({
        #                         'time': entry['created_at'],
        #                         'id': cso,
        #                         'num_of_chats': num_of_chats
        #                     })

        #             for d in data:
        #                 print(d)


        #             msg_distribution = NewCustomerDistribution(amt_of_members=5, max_amt_of_chats_per_member=5, cso_id_chatamt_timestamp=data)
        #             next_cso = msg_distribution.add_new_chat()
        #         #     print(f'next_cso (NewCustomerDistribution): {next_cso}')
        #         #     instance.assigned_cso = next_cso      # OK
        #         #     instance.save()
        #             # ############################################################################
        #         # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                
        #         # Add prevoius msg-dipsdsaiufyasiduyasdiuysaduy ************************




        #         # LAST RESORT [if the prev-msg-distribution-algo doesn't work]
        #         # active_cso_list = [x['cso_email'] for x in filtered_hdo]
        #         # print("active_cso_list:", active_cso_list)
        #         # selected_active_cso_email = random.choice(active_cso_list)
        #         # print("selected HDO:", selected_active_cso_email)
                
        #         # instance.assigned_cso = selected_active_cso_email
        #         instance.assigned_cso = next_cso
        #         instance.save()     # will got to update-code-block
        #         pass


            
        #     # # [Already copied above] -------------------------------------------------------------------------------
        #     # active_cso_list = [x['cso_email'] for x in active_cso]
        #     # cso_email_total_msg_list = [x['assigned_cso'] for x in total_msg]
        #     # fresh_cso_no_msg = list(set(active_cso_list).symmetric_difference(set(cso_email_total_msg_list)))

        #     # if len(fresh_cso_no_msg) >= 1:
        #     #     selected_active_cso_email = random.choice(fresh_cso_no_msg)
        #     #     next_cso = selected_active_cso_email    # COMMENT IT
        #     #     instance.assigned_cso = next_cso      # OK
        #     #     instance.save()
        #     #     room_name_normalized="".join(ch for ch in next_cso if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
        #     #     # Get all the message reqs of the individual CSO
        #     #     data = CustomerSupportRequest.get_customer_support_reqs()
        #     #     # print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")
        #     #     result = []
        #     #     for i in data:
        #     #         if i['assigned_cso'] == next_cso:
        #     #             # print(i)
        #     #             result.append(i)

        #     #     # [03]
        #     #     async_to_sync(channel_layer.group_send)(
        #     #         f'chat_dashboard_{room_name_normalized}',
        #     #         {
        #     #             'type': 'new_support_req', 
        #     #             'new_support_request': result,
        #     #         }
        #     #     )

        #     # else:
        #     #     # for dt in new_dict:
        #     #     #     print(dt)

        #     #     msg_req = []
        #     #     for msg in total_msg:
        #     #         msg_req.append(msg['assigned_cso'])
        #     #     msg_req_set = set(msg_req)
        #     #     msg_count = []
        #     #     msg_req_list = list(msg_req_set)
        #     #     for i in msg_req_list:
        #     #         msg_count.append(msg_req.count(i))

        #     #     cso_num_of_chats = zip(msg_req_list, msg_count)
        #     #     cso_num_of_chats_list = []
        #     #     for i in cso_num_of_chats:
        #     #         cso_num_of_chats_list.append(i)

        #     #     for cnocl in cso_num_of_chats_list:
        #     #         print(cnocl)

        #     #     data_1, data_2 = new_dict, cso_num_of_chats_list
        #     #     data_1_processed = []
        #     #     for entry in data_1:
        #     #         data_1_processed.append({
        #     #             'cso': entry['cso'],
        #     #             'created_at': entry['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        #     #         })
        #     #     # print('data_1_processed \n',data_1_processed)
        #     #     # Create dictionary mapping CSOs to number of chats from data_2
        #     #     cso_to_chats = dict(data_2)

        #     #     # print('CSO to chats \n', cso_to_chats, '\n')
        #     #     # Combine data_1 and data_2 to create final list
        #     #     data = []
        #     #     ids_processed = set()
        #     #     # print('ids_processed',ids_processed,'\n')

        #     #     for entry in data_1_processed:
        #     #         cso = entry['cso']
        #     #         num_of_chats = cso_to_chats.get(cso, 0)
        #     #         if cso not in ids_processed:
        #     #             ids_processed.add(cso)
        #     #             data.append({
        #     #                 'time': entry['created_at'],
        #     #                 'id': cso,
        #     #                 'num_of_chats': num_of_chats
        #     #             })

        #     #     for d in data:
        #     #         print(d)


        #     #     msg_distribution = NewCustomerDistribution(amt_of_members=5, max_amt_of_chats_per_member=5, cso_id_chatamt_timestamp=data)
        #     #     next_cso = msg_distribution.add_new_chat()
        #     #     print(f'next_cso: {next_cso}')

        #     #     # Broadcast the "data" into the "CSODashboardConsumer" consumer channel-group
        #     #     # Solution: https://stackoverflow.com/a/7811582
        #     #     # [Explanation] Create a method in the consumer-class which will be responsible 
        #     #     # for sending the payload to each individual cso-channel's frontend wbSocket 
        #     #     # through "CSODashboardConsumer".
        #     #     # channel_layer = get_channel_layer()   # MOVED TO THE TOP

        #     #     # TODO: This signal will be custom-made later, logic will be implemented here to decide in which cso-support-dashboard-channel the request will be sent to.
        #     #     # cso_email = "tanjim.ashraf@doer.com.bd" # COMMENT IT
        #     #     # cso_email = "tanjim.ashraf.doer.bp@gmail.com" # COMMENT IT
        #     #     # next_cso = cso_email    # COMMENT IT
        #     #     # instance.assigned_cso = cso_email
        #     #     instance.assigned_cso = next_cso      # OK
        #     #     instance.save()

        #     #     # Get all the message reqs of the individual CSO
        #     #     data = CustomerSupportRequest.get_customer_support_reqs()
        #     #     # print(f"all support request (called the 'get_customer_support_reqs()' staticmethod!): {data}")
        #     #     result = []

        #     #     for i in data:
        #     #         if i['assigned_cso'] == next_cso:
        #     #             # print(i)
        #     #             result.append(i)
        #     #     # print(f'Result (based of assigned CSO: {result})')
        #     #     print('#'*50)
        #     #     print('\n'*2)
                
        #     #     room_name_normalized="".join(ch for ch in next_cso if ch.isalnum())   # keeps only alphanumeric-chars in the room-name. [Ref]: https://www.scaler.com/topics/remove-special-characters-from-string-python/
                
        #     #     # [04]
        #     #     async_to_sync(channel_layer.group_send)(
        #     #         f'chat_dashboard_{room_name_normalized}',
        #     #         {
        #     #             'type': 'new_support_req', 
        #     #             'new_support_request': result,
        #     #         }
        #     #     )
        #     # # -------------------------------------------------------------------------------

        
        
        # # return True
        # # -------------------------------------------------------------------------------------------------------------------
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    # On update
    if not created:
        print('\n'*3)
        print('+'*50)
        print(f'Update the customer support request called from "customer_support_request_signal_post_save()" func! {instance.is_resolved}')

        instance_room_slug = instance.room_slug
        instance_resolved = instance.is_resolved
        instance_dismissed = instance.is_dismissed
        instance_detached = instance.is_detached
        instance_assigned_cso = instance.assigned_cso
        # instance_registered_user_email = instance.registered_user_email
        print("instance_resolved (not created):", instance_resolved)
        print("instance_dismissed (not created):", instance_dismissed)
        print("instance_detached (not created):", instance_detached)

        
        # room_name_normalized="".join(ch for ch in instance_registered_user_email if ch.isalnum())   # [incorrect]: support-reqs should appear to an HDO's support dashboard; not on a user's dashboard
        room_name_normalized="".join(ch for ch in instance_assigned_cso if ch.isalnum())              # [correct]

        # [NEWLY CREATED MSG-REQ] but its inside the update-code-block bcz an HDO is assigned & saved in the create-code-block
        if not instance_detached and not instance_dismissed and not instance_resolved:
            # Pass newly created cusSpprtReq to the HDO dashboard

            data = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=instance_assigned_cso)    # get all the reqs of that HDO who is assigned to this instance's "assigned_cso" attr.

            # Delete the "created_at" key-value pair from each dict of the filtered msg-reqs
            for d in data:
                del d['created_at']
            
            # [06]
            async_to_sync(channel_layer.group_send)(
                f'chat_dashboard_{room_name_normalized}',
                {
                    'type': 'new_support_req', 
                    'new_support_request': data,
                }
            )


        else:
            result_r_d = "Resolve Socket" if instance_resolved else "Dismiss Socket" if instance_dismissed else True
            print(f"Resolve/Dismiss Result: {result_r_d}")
            # Get all the message reqs of the individual CSO
            # data = CustomerSupportRequest.get_unresolved_customer_support_reqs()
            data = CustomerSupportRequest.get_customer_support_reqs()
            # Get the length of total current reqs
            total_current_reqs = len(data)
            print("Total current req", total_current_reqs)
            print("Total current req (type)", type(total_current_reqs))

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
        print('+'*50)
        print('\n'*3)





@receiver(post_delete, sender=CustomerSupportRequest)
def customer_support_request_signal_post_delete(sender, instance, **kwargs):
    print('\n'*3)
    print('+'*50)
    print('Delete a record from the customer support request model, called by the "customer_support_request_signal_post_delete()" func!')
    print(instance.room_slug)
    # Modify the associate record inside the "CSOVisitorConvoInfo" model (try-catch)
    try:
        cso_user_chat_info = CSOVisitorConvoInfo.objects.get(room_slug=instance.room_slug)
        cso_user_chat_info.is_cleared = True
        cso_user_chat_info.is_connected = False
        cso_user_chat_info.save()
        print("Successfully modify the record inside the 'CSOVisitorConvoInfo' model.")
        # Send a socket signal to the CSO-user chatroom, thus the user is redirected to the home-page & the CSO is redirected to the Support-Request-List page
        channel_layer = get_channel_layer()
        # Check if the record contains "is_cancelled" is True
        print(f"cso_user_chat_info.is_cancelled: {cso_user_chat_info.is_cancelled}")
        print(f"cso_user_chat_info.is_dismissed: {cso_user_chat_info.is_dismissed}")
        if (cso_user_chat_info.is_cancelled):
            async_to_sync(channel_layer.group_send)(
                f'chat_{cso_user_chat_info.room_slug}',
                {
                    'type': 'support_request_cleared', 
                    # 'total_current_reqs': total_current_reqs,
                    'CSOVisitorConvoInfo_isCancelled': True,
                }
            )
        print('room-slug assigned to msg-req:',instance.room_slug)
        print('assigned cso of msg-req:',instance.assigned_cso)
        data = CustomerSupportRequest.get_unresolved_customer_support_reqs()
        # Get the length of total current reqs
        total_current_reqs_after_convo_cancelled = len(data)
        print("total current msg-req:", total_current_reqs_after_convo_cancelled)
        room_name_normalized="".join(ch for ch in instance.assigned_cso if ch.isalnum())
        # Send a socket signal to spicific CSO's "CSR list"
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
    print('+'*50)
    print('\n'*3)




# @receiver(post_save, sender=CSOVisitorConvoInfo)
# def cso_visitor_chat_convo_signal_post_save(sender, instance, created, **kwargs):
#     if not created:
#         print('\n'*3)
#         print('+'*50)
#         print('Update chat-convo-info record from the "CSOVisitorConvoInfo" model, send to the specifc CSO\'s CSR dashboard to remove the msg-req in real-time')
#         print(instance.room_slug)
#         print(instance.cso_email)
#         data = CustomerSupportRequest.get_unresolved_customer_support_reqs()
#         # Get the length of total current reqs
#         total_current_reqs = len(data)
#         print("total current msg-req:", total_current_reqs)
#         print('+'*50)
#         print('\n'*3)

