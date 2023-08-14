from home.models import CustomerSupportRequest
import random, datetime as DT
from datetime import datetime as dt


class MessageAmountChecker:
    def __init__(self, instance):
        # self.filtered_hdo = filtered_hdo_list
        # self.location_based_active_hdo_filtration = loc_based_hdo_filtration_obj
        self.instance = instance

    def customer_support_request_counter(self, hdo_email):
        return len(CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=hdo_email))

    def lastest_msg_timestamp(self, hdo_email):
        # CustomerSupportRequest.get_reqs_with_creation_timestamp(cso_email=hdo_email)
        timestamp_list = [grwct['created_at'] for grwct in CustomerSupportRequest.get_reqs_with_creation_timestamp(cso_email=hdo_email)]
        # Find the latest timestamp from the list & lastely return it.

        # return max(timestamp_list)
        try:
            return max(timestamp_list)
        except ValueError as VE:    
            # [IT MEANS IF THERE IS A FRESH ACTIVE HDO WHO DOESN'T HANDLE ANY CUSTOMER-SUPPORT-REQUEST YET, THEN THE 'timestamp_list[]' WILL RETURN EMPTY LIST, 
            # WHICH WILL THROW ERROR IF 'max()' METHOD IS APPLIED THERE, THUS RETURNING THE TIMESTAMP OF (cur_y, cur_m, cur_day, 0,0) WILL ALLOW THE CODE-BLOCK:
            # "oldest_timestamp = min([mclz[2] for mclz in msg_count_list_zipped])" TO EXTRACT THIS FRESH NEW HDO TO BE SENT THE NEXT MSG-REQ]
            if not timestamp_list:
                # return datetime.datetime variable as something like (current_year, current_month, current_date, 0, 0)
                y, m, d = dt.now().year, dt.now().month, dt.now().day
                # return DT.datetime(y,m,d)     # [THROWS ERROR]: BECAUSE THIS DATETIME DOESN'T HAVE ANY "datetime.timezone" INFORMATION WITH IT, WHICH CAUSES COMPARISON ERROR WITH THE OTHER "datetime" TIMESTAMPS IN THE PARENT METHOD TO FIND THE "min() / oldest" TIMESTAMP OUT OF THEM.
                return DT.datetime(y,m,d,0,0, tzinfo=DT.timezone.utc)

    def assign_cso(self, instance, filtered_hdo):
        # print(f"MessageAmountChecker.assign_cso(): {filtered_hdo}")
        # Check if the HDO is currently hadnling ">=5" msg-request which are not detached yet; 
        # if found True (means, that the HDO is currently handling more that or equal to 5 support_requests): then return false, 
        # so that the next_msg_req doesn't get assigned to that HDO.
        if self.customer_support_request_counter(hdo_email=filtered_hdo) >= 5:
            return False
        instance.assigned_cso = filtered_hdo
        instance.save()
        return True
    
    def singular_msg_amount_checker(self, filtered_hdo):
        # msg_count = len(CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=filtered_hdo[0]['cso_email']))
        msg_count = self.customer_support_request_counter(hdo_email=filtered_hdo[0]['cso_email'])
        if msg_count >= 5:
            return False
        else:
            # self.instance.assigned_cso = filtered_hdo[0]['cso_email']
            # self.instance.save()
            return self.assign_cso(instance=self.instance, filtered_hdo=filtered_hdo[0]['cso_email'])
            return True
    
    def multiple_msg_amount_checker(self, filtered_hdo):
        curated_hdo_emails = [fh['cso_email'] for fh in filtered_hdo]
        # msg_count_list = [self.customer_support_request_counter(hdo_email=che) for che in curated_hdo_emails]

        msg_count_list_zipped = [(che, \
                                  self.customer_support_request_counter(hdo_email=che), \
                                    self.lastest_msg_timestamp(hdo_email=che)) for che in curated_hdo_emails]
        
        # "msg_count_list_zipped" data format:   
        # [
        #   ('hdo34@gmail.com', 1, datetime.datetime(2023, 7, 15, 8, 15, 53, 93488, tzinfo=datetime.timezone.utc)),
        #   ('hdo34@gmail.com', 1, datetime.datetime(2023, 7, 15, 8, 15, 53, 93488, tzinfo=datetime.timezone.utc)),
        #   ('hdo34@gmail.com', 1, datetime.datetime(2023, 7, 15, 8, 15, 53, 93488, tzinfo=datetime.timezone.utc)),
        # ]

        least_msg_count = min([mclz[1] for mclz in msg_count_list_zipped])  # get the "min_amnt_of_msg_count" to verify if all of these filtered_hdos has 5 or more than 5 support-reqs handling currently
        
        if least_msg_count >= 5:    # if every selected hdo (filtered) has ">=5" chats then those HDOs are incapble of handling any further support request unless detaching/ dismissing/ resolving any of their currently occupied support-request.
            return False
        else:
            filter_hdo_with_least_msg = [mclz for mclz in msg_count_list_zipped if mclz[1] == least_msg_count]
            if len(filter_hdo_with_least_msg) == 1:
                return self.assign_cso(instance=self.instance, filtered_hdo=filter_hdo_with_least_msg[0][0])
                # self.instance.assigned_cso = filter_hdo_with_least_msg[0][0]
                # self.instance.save()
                return True
            if len(filter_hdo_with_least_msg) > 1:
                # For the HDOs with least msg-handling currently, thus implement the timestamp-based-distribution.
                # ******* SCOPE TO REFINE FURTHER (-T-U-N-I-N-G-) BASED ON "Timestamp-Priority-Distribution" *******
                # oldest_timestamp = min([mclz[2] for mclz in msg_count_list_zipped])     # [WRONG LIST[]] get the oldest timestamp of the cureated_HDOs' of their lastest_msg_handling, so that the HDO with the oldest_msg_handling will get the next msg_req
                oldest_timestamp = min([fhwlm[2] for fhwlm in filter_hdo_with_least_msg])     # get the oldest timestamp of the cureated_HDOs' of their lastest_msg_handling, so that the HDO with the oldest_msg_handling will get the next msg_req
                selected_hdo = []   # if still found multiple records with the same oldest_timestamp of msg_handling, then simply randomly sleesct an HDO to send the next_msg_req.
                for mclz in msg_count_list_zipped:
                    if mclz[2] == oldest_timestamp:
                        selected_hdo.append(mclz[0])

                if len(selected_hdo) == 1:
                    return self.assign_cso(instance=self.instance, filtered_hdo=selected_hdo[0])
                if len(selected_hdo) > 1:
                    selected_hdo_random = random.choice(selected_hdo)
                    return self.assign_cso(instance=self.instance, filtered_hdo=selected_hdo_random)
                    # ******* SCOPE TO REFINE FURTHER (-T-U-N-I-N-G-): Check the multiple_filtered_HDOs currently_handling_msg_amnt to send it to other random HDO (might be -O-V-E-R-T-U-N-I-N-G-) *******
                    # NB: **this will help to reduce computing on bigger geo-location to find more HDOs if return to its parent method as False.
                    # possible apporach: rmeove that hdo-email from this "selected_hdo" list & try again randomly select another HDO to send th emsg-req to.
                    # result = self.assign_cso(instance=self.instance, filtered_hdo=selected_hdo_random)
                    # if not result:
                    #     selected_hdo_random = random.choice(selected_hdo)
                return True
