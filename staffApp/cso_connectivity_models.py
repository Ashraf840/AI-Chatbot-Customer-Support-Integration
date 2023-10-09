from django.db import models
from home.models import CustomerSupportRequest


class CSOOnline(models.Model):
    """
    This class store record of HDO (CSO) along with their organization-name, location, district & division. This extra pair of values are required while filtering active/onlined HDOs using the "get_active_cso" method
    """
    cso_email = models.CharField(verbose_name='HDO email', max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    is_active = models.BooleanField(verbose_name='HDO active', default=True)
    joined_at = models.DateTimeField(verbose_name="Joined at", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last activity", auto_now=True)
    # User Organization & Static Geographic location
    user_organization = models.CharField(verbose_name='Organization', max_length=100, blank=True, null=True)
    location = models.CharField(verbose_name='Location', max_length=100, blank=True, null=True)
    district = models.CharField(verbose_name='District', max_length=100, blank=True, null=True)
    division = models.CharField(verbose_name='Division', max_length=100, blank=True, null=True)

    class Meta:
        # verbose_name_plural = "CSO Online (inside System)"
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
        # print("cso_filtration method is called!")
        # TODO: Instead of a list, use a dictionary for checking redundency & appending as key-value pair, later in its parent-method, extract only the values iut of that filtered dictionary.
        # filtered_instances = list() # MIGHT CONTAIN REDUNDANCY
        filtered_instances = dict() # MIGHT CONTAIN REDUNDANCY
        for i in instances:
            # print(f"i['user_organization'] - HDO Record: {i['user_organization']}")
            # print(f"User organization - Passed args: {user_organization}")

            # append as much possible HDOs as we can, since the user will suppose to route to a divisional-HDO ->
            # TODO: [followed by the last LOC] or at least a general onlined-HDO (for at least appending an active HDO, require to define a check condition on another general query "get_active_cso()" w/t passing args to fetch all the active HDOs)
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

        # print(f"filtered_instances: {filtered_instances}")
        return filtered_instances

    @staticmethod
    def get_cso_online(
            user_organization, 
            location, 
            district, 
            division):
        """
        This method is used to return all the records of currently online/offline CSO (HDO). It expects user's organization name, location, district, division as required parameters.
        """
        # If any of the param is None, then list out all the values excluding user_organization, location, district, division
        if user_organization is None \
            or location is None \
            or district is None \
            or division is None:
            print("WOrked-1")
            instances = list(CSOOnline.objects.values('cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update', 'user_organization', 'location', 'district', 'division'))   # Solution: https://stackoverflow.com/a/7811582
            # in last LOC appending {user_organization, location, district, division} set, so that in terms of general HDO matching inside "LocationBasedActiveHDOFiltration.gen_match()", we can make further classification of none-location-based-hdo & vice versa. 
            return instances
        else:
            print("WOrked-2")
            # [Expensive Computation] Filtration based on org, loc, dist, div before returning the "instances" list
            instances = list(CSOOnline.objects.values(
                'cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update',
                'user_organization', 'location', 'district', 'division'
            ))

            # This filtration will get all the HDOs regardless of their {org, loc, dist or div} as long as the user's {div} matches HDOs' {div}
            instances = CSOOnline.cso_filtration(
                user_organization=user_organization,
                location=location,
                district=district,
                division=division,
                instances=instances
            )
            return instances

    @staticmethod
    def get_active_cso(
            user_organization=None, 
            location=None, 
            district=None, 
            division=None,
            # The last 2-params are used for getting length of active_cso in the "ChatRoomCreateAPISocket" in chat_room_create_api to get the confirmation of available HDOs, if no HDO is avaialble, then emmit "No CSO Available" through chatbot in the chatbot-box.
            loc_support_confirmation=False,
            gen_support_confirmation=False):
        """
        This method is used to return all the records of currently online CSO. This approach is taken because the database of this project is used as mongodb, 
        since mongodb is not supported native django-filtering.
        """
        instances = CSOOnline.get_cso_online(
            user_organization=user_organization,
            location=location,
            district=district,
            division=division)
        active_cso = []
        # If the method gets invoked anywhere in the project w/t passed args in params (Mainly for getting the length of active/online CSOs (HDO), although the active HDO-list-object is returned to its parent-method.)
        # If any of the loc-set-attr {org, loc, dist, div} is missing, it'll enter into this code block
        if user_organization is None \
            or location is None \
            or district is None \
            or division is None:
            print("WOrked-1: get_active_cso")
            for i in instances:
                if i['is_active']:
                    active_cso.append(i)
            # active_cso_result = [active_cso.append(i) for i in instances if i['is_active']]
            # active_cso = active_cso_result
            print(f"Length of general active_cso_list: {len(active_cso)}")
            # print(f"General active_cso_list:", active_cso)

            # [Halt in chat-room-api-creation] ------------------------------------------------------------------------------------------
            if gen_support_confirmation:
                print("gen_support_confirmation code-block is executed!")
                # TODO: Return zero if no HDO is currently avaiable based on the amnt-of-spprt-req-handling
                clear_flag = True

                for ac in active_cso:
                    if CSOOnline.customer_support_request_counter(hdo_email=ac['cso_email']) < 5:   
                        clear_flag = False
                
                if clear_flag:
                    active_cso.clear()
            # ------------------------------------------------------------------------------------------

            return active_cso
        else:
            print("WOrked-2: get_active_cso")
            # THIS WAS THROWING ERROR/ WORKING W/ WRONG RETURNED DATATYPE
            # for i in instances.items():
            # for i in instances:
            #     # if i['is_active']:
            #         active_cso.append(i)
            # return active_cso

            # APPROACH-1 (Old)
            # filtered_cso_list = list()
            # for i in instances.items():
            #     filtered_cso_list.append(i[1])

            # APPROACH-2 (Modern/list comprehension);   filter out the hdo-online-record attached with his/her hdo-email as a tuple. Thus extract & append only the hdo-online-record.
            filtered_cso_list = [i[1] for i in instances.items()]
            # print(f"Length of filtered_cso_list: {len(filtered_cso_list)}")
            # return filtered_cso_list

            # APPROACH-1 (Old); After filtering the hdo-online-record, filter only the records w/ "is_active=True" & append in the "active_cso" list.
            for i in filtered_cso_list:
                if i['is_active']:
                    active_cso.append(i)

            # APPROACH-2 (Modern/list comprehension)    - [NOT USING]
            # active_cso = [active_cso.append(i) for i in filtered_cso_list if i['is_active']]    # location-based filtration algorithm

            # if "active_cso" returns an empty list after filtration based on 'org', 'loc', 'dist', 'div', then invoke this "get_active_cso" static-method again here, but this time w/t passing any args as params to this method, so that the method can fetch all the active CSOs regardless of their {org, loc, dist, div} values.
            # [check active_hdo] if no matched_loc_based_active_hdo is found, then get all the active HDOs
            if len(active_cso) == 0:
                # [Generally] CSOs w/t any {org, loc, dist, div}
                print("No loc-based-matching-HDO is currently available!")
                return CSOOnline.get_active_cso(gen_support_confirmation=True)
            
            # [Halt in chat-room-api-creation] -------------------------------------------------------------------------------------------------------------
            if loc_support_confirmation:
                print("loc_support_confirmation code-block is executed!")
                # TODO: Redirect to get the general-active-hdo if all the currently (exact/partial)_matched_loc_based_hdo is pre-occupied with ">=5" support-chats. 
                # [check if those active_hdo aren't pre-occupied with >=5 chats] if the active_loc_based_hdo are all occupied with >=5 chat-reqs, then get all the 
                recall_flag = True
                
                for ac in active_cso:
                    if CSOOnline.customer_support_request_counter(hdo_email=ac['cso_email']) < 5:   
                        recall_flag = False


                # [strike-through; correction required in this comment block] if any of the "loc_based_hdo" is currently handling less than 5 support-requests, then make the 
                # "reset_flag=False" so that it doesn't clear the "active_cso" list (otherwise, it will cause the 
                # chatbot to return "No CSO available!" to customer in the chatbot-box). [strike-through; correction required in this comment block]

                if recall_flag:
                    # active_cso.clear()  # it'll be called lastly in the "get_active_cso()" with no-loc-related-args in the param
                    return CSOOnline.get_active_cso(gen_support_confirmation=True)
            # -------------------------------------------------------------------------------------------------------------

            return active_cso



class CSOConnectedChannels(models.Model):
    cso_email = models.CharField(verbose_name='HDO email', max_length=60, blank=True, null=True)
    room_slug = models.CharField(max_length=60)
    channel_value = models.CharField(max_length=74)

    class Meta:
        # verbose_name_plural = "CSO Channels (inside System)"
        verbose_name_plural = "HDO Channels (inside System)"
