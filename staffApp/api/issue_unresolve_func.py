from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .helper_func.tms_issue_operation import TMSIssueOperation
from rest_framework.response import Response


class TMSIssueUnresolveAPI(APIView):
    def post(self, request, format=None):
        tms_issue_opt = TMSIssueOperation(
            ticket_issue_oid=request.data["ticket_issue_oid"],
            user_signing_token_tms=request.data["user_signing_token_tms"],
            remark_input_dismiss_value=request.data["remark_input_dismiss_value"],
        )

        data = tms_issue_opt.unresolve_tms_issue(
            common_cso_email=request.data["common_cso_email"],
            common_registered_user_email=request.data["common_registered_user_email"],
            roomSlugParam=request.data["roomSlugParam"],
        )
        #print("TMSIssueUnresolveAPI:", data)
        return Response(data)
        return HttpResponse("OK: 'TMSIssueUnresolveAPI' api is executed")

        return JsonResponse({
            'ticket_issue_oid': f'{request.data["ticket_issue_oid"]}',
            'user_signing_token_tms': f'{request.data["user_signing_token_tms"]}',
            'remark_input_dismiss_value': f'{request.data["remark_input_dismiss_value"]}',
            'common_cso_email': f'{request.data["common_cso_email"]}',
            'common_registered_user_email': f'{request.data["common_registered_user_email"]}',
            'roomSlugParam': f'{request.data["roomSlugParam"]}',
        })
    

