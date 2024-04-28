from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .helper_func.tms_issue_operation import TMSIssueOperation
from rest_framework.response import Response


class TMSIssueResolveAPI(APIView):
    # def get(self, request, remark_input_resolve_value, ticket_issue_oid, user_signing_token_tms, format=None):
    #     # data = fetch_tms_issue(ticket_issue_oid, user_signing_token_tms)
    #     # return Response(data)
    
    def post(self, request, format=None):
        print("TMSIssueResolveAPI class is called!")
        print(f'ticket_issue_oid: {request.data["ticket_issue_oid"]}')
        print(f'user_signing_token_tms: {request.data["user_signing_token_tms"]}')
        print(f'remark_input_resolve_value: {request.data["remark_input_resolve_value"]}')
        print(f'cso_email: {request.data["cso_email"]}')
        print(f'registered_user_email: {request.data["registered_user_email"]}')
        print(f'roomSlugParam: {request.data["roomSlugParam"]}')

        tms_issue_opt = TMSIssueOperation(
            ticket_issue_oid=request.data["ticket_issue_oid"],
            user_signing_token_tms=request.data["user_signing_token_tms"],
            remark_input_resolve_value=request.data["remark_input_resolve_value"],
        )

        data = tms_issue_opt.resolve_tms_issue(
            cso_email=request.data["cso_email"],
            registered_user_email=request.data["registered_user_email"],
            roomSlugParam=request.data["roomSlugParam"],
        )

        return Response(data)

