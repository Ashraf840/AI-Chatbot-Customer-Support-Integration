import requests
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from home.models import CSOVisitorConvoInfo, CustomerSupportRequest, RemarkResolution



class TMSIssueOperation:
    def __init__(self, ticket_issue_oid, user_signing_token_tms, remark_input_resolve_value=None, remark_input_dismiss_value=None):
        self.ticket_issue_oid = ticket_issue_oid 
        self.user_signing_token_tms = user_signing_token_tms
        self.remark_input_resolve_value = remark_input_resolve_value
        self.remark_input_dismiss_value = remark_input_dismiss_value
        self.channel_layer = get_channel_layer()

    def resolve_tms_issue(self, cso_email, registered_user_email, roomSlugParam):
        print("test: TMSIssueOperation.fetch_tms_issue()")

        # # Define inside the "Activate Socketting" code-block
        modified_cso_visitor_convo_info = self.modify_cso_visitor_convo_info(resolve=True, roomSlugParam=roomSlugParam, cso_email=cso_email)
        self.modify_cust_support_req(room_slug_param=roomSlugParam, resolve=True)
        self.create_remark_resolution(modified_cso_visitor_convo_info, self.remark_input_resolve_value)


        # print("ticket_issue_oid:", self.ticket_issue_oid)
        # print("user_signing_token_tms:", self.user_signing_token_tms)
        # print("remark_input_resolve_value:", self.remark_input_resolve_value)
        # print("cso_email:", cso_email)
        # print("registered_user_email:", registered_user_email)
        # print("roomSlugParam:", roomSlugParam)

        # # url = "https://tms-test.celloscope.net/api/v1/issue-resolve-by-call-center-agent"
        
        # ---------------------------------------------------------------------------------
        url = "http://172.16.6.134/api/v1/issue-resolve-by-call-center-agent"

        payload = json.dumps({
            "remarks": f"{self.remark_input_resolve_value}",
            "issueOid": f"{self.ticket_issue_oid}"
        })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self.user_signing_token_tms}',
            'Content-Type': 'application/json',
            'Referer': f'http://172.16.6.134/issue/{self.ticket_issue_oid}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # response_text = response.text()
        response_json = response.json()

        if response_json["status"] and response_json["code"] == 200:
            print("Activate socketting!")

            async_to_sync(self.channel_layer.group_send)(
                f'chat_{roomSlugParam}',
                {
                    'type': 'support_resolved', 
                    'cso_email': cso_email,
                    'reg_user_email': registered_user_email,
                    'ticket_issue_oid': self.ticket_issue_oid,
                    'user_signing_token_tms': self.user_signing_token_tms,
                    'remark_input_resolve_value': self.remark_input_resolve_value,
                    'roomSlugParam': roomSlugParam,
                }
            )

        return response.json()
    
    def unresolve_tms_issue(self, common_cso_email, common_registered_user_email, roomSlugParam):
        print("test: TMSIssueOperation.unresolve_tms_issue()")

        # Define inside the "Activate Socketting" code-block
        modified_cso_visitor_convo_info = self.modify_cso_visitor_convo_info(dismiss=True, roomSlugParam=roomSlugParam, cso_email=common_cso_email)
        self.modify_cust_support_req(room_slug_param=roomSlugParam, dismiss=True)
        self.create_remark_resolution(modified_cso_visitor_convo_info, self.remark_input_dismiss_value)
        

        print("ticket_issue_oid:", self.ticket_issue_oid)
        print("user_signing_token_tms:", self.user_signing_token_tms)
        print("remark_input_dismiss_value:", self.remark_input_dismiss_value)
        print("common_cso_email:", common_cso_email)
        print("common_registered_user_email:", common_registered_user_email)
        print("roomSlugParam:", roomSlugParam)

        # return "response from: TMSIssueOperation.unresolve_tms_issue()"

        # # url = "https://tms-test.celloscope.net/api/v1/issue-resolve-by-call-center-agent"
        
        # ---------------------------------------------------------------------------------
        url = "http://172.16.6.134/api/v1/update-issue-status-by-oid"

        payload = json.dumps({
            "remarks": f"{self.remark_input_dismiss_value}",
            "oid": f"{self.ticket_issue_oid}"
        })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self.user_signing_token_tms}',
            'Content-Type': 'application/json',
            'Referer': f'http://172.16.6.134/issue/{self.ticket_issue_oid}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # response_text = response.text()
        response_json = response.json()
        print("json-response from: TMSIssueOperation.unresolve_tms_issue()")
        print(f"{response_json}")

        if response_json["status"] and response_json["code"] == 200:
            print("Activate socketting!")
            
            async_to_sync(self.channel_layer.group_send)(
                f'chat_{roomSlugParam}',
                {
                    'type': 'chat_convo_dismissed', 
                    'common_cso_email': common_cso_email,
                    'common_registered_user_email': common_registered_user_email,
                    'ticket_issue_oid': self.ticket_issue_oid,
                    'user_signing_token_tms': self.user_signing_token_tms,
                    'remark_input_dismiss_value': self.remark_input_dismiss_value,
                    'roomSlugParam': roomSlugParam,
                }
            )

        return response.json()

    def modify_cso_visitor_convo_info(self, roomSlugParam, cso_email, resolve=None, dismiss=None):
        cso_visitor_convo_info = CSOVisitorConvoInfo.objects.get(room_slug=roomSlugParam, cso_email=cso_email)  # mark the convo-info as resolved, & make the CSO disconnected from the conversation
        if resolve is not None:
            # print("modify_cso_visitor_convo_info: Resolve is not None!")
            # print(f"cso_visitor_convo_info: {cso_visitor_convo_info}")
            cso_visitor_convo_info.is_resolved, cso_visitor_convo_info.is_connected = True, False
            cso_visitor_convo_info.save()
            return cso_visitor_convo_info

        if dismiss is not None:
            # print("modify_cso_visitor_convo_info: Dismiss is not None!")
            # print(f"cso_visitor_convo_info: {cso_visitor_convo_info}")
            cso_visitor_convo_info.is_dismissed, cso_visitor_convo_info.is_connected = True, False
            cso_visitor_convo_info.save()
            return cso_visitor_convo_info

    def create_remark_resolution(self, cso_visitor_convo_info, remarks):
        RemarkResolution.objects.create(
            cso_user_convo=cso_visitor_convo_info,
            remarks=remarks
        )

    def modify_cust_support_req(self, room_slug_param: str, resolve=None, dismiss=None):
        # print("modify_cust_support_req (room-slug):", room_slug_param)
        cust_support_req = CustomerSupportRequest.objects.get(room_slug=room_slug_param)
        if resolve is not None:
            if not cust_support_req.is_resolved:
                cust_support_req.is_resolved = True
                cust_support_req.save()

        if dismiss is not None:
            if not cust_support_req.is_dismissed:
                cust_support_req.is_dismissed = True
                cust_support_req.save()
