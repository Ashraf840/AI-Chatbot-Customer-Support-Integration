from home.models import CustomerSupportRequest
import random, datetime as DT
from datetime import datetime as dt


class MessageAmountChecker:
    def __init__(self, instance):
        self.instance = instance

    def customer_support_request_counter(self, hdo_email):
        return len(CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=hdo_email))

    def lastest_msg_timestamp(self, hdo_email):
        timestamp_list = [grwct['created_at'] for grwct in CustomerSupportRequest.get_reqs_with_creation_timestamp(cso_email=hdo_email)]
        try:
            return max(timestamp_list)
        except ValueError as VE:    
            if not timestamp_list:
                y, m, d = dt.now().year, dt.now().month, dt.now().day
                return DT.datetime(y,m,d,0,0, tzinfo=DT.timezone.utc)        

    def assign_cso(self, instance, filtered_hdo):
        if self.customer_support_request_counter(hdo_email=filtered_hdo) >= 5:
            return False
        instance.assigned_cso = filtered_hdo
        instance.save()
        return True
    
    def singular_msg_amount_checker(self, filtered_hdo):
        msg_count = self.customer_support_request_counter(hdo_email=filtered_hdo[0]['cso_email'])
        if msg_count >= 5:
            return False
        else:
            return self.assign_cso(instance=self.instance, filtered_hdo=filtered_hdo[0]['cso_email'])
    
    def multiple_msg_amount_checker(self, filtered_hdo):
        curated_hdo_emails = [fh['cso_email'] for fh in filtered_hdo]

        msg_count_list_zipped = [(che, \
                                  self.customer_support_request_counter(hdo_email=che), \
                                    self.lastest_msg_timestamp(hdo_email=che)) for che in curated_hdo_emails]
        
        least_msg_count = min([mclz[1] for mclz in msg_count_list_zipped])

        if least_msg_count >= 5:
            return False
        else:
            filter_hdo_with_least_msg = [mclz for mclz in msg_count_list_zipped if mclz[1] == least_msg_count]
            if len(filter_hdo_with_least_msg) == 1:
                return self.assign_cso(instance=self.instance, filtered_hdo=filter_hdo_with_least_msg[0][0])
            
            if len(filter_hdo_with_least_msg) > 1:
                oldest_timestamp = min([fhwlm[2] for fhwlm in filter_hdo_with_least_msg])
                selected_hdo = []
                for mclz in msg_count_list_zipped:
                    if mclz[2] == oldest_timestamp:
                        selected_hdo.append(mclz[0])

                if len(selected_hdo) == 1:
                    return self.assign_cso(instance=self.instance, filtered_hdo=selected_hdo[0])
                if len(selected_hdo) > 1:
                    selected_hdo_random = random.choice(selected_hdo)
                    return self.assign_cso(instance=self.instance, filtered_hdo=selected_hdo_random)
                return True

