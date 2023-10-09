from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .helper_func.tms_issue_operation import TMSIssueOperation
from rest_framework.response import Response


# @method_decorator(csrf_exempt, name='post')
class TMSIssueUnresolveAPI(APIView):
    def post(self, request, format=None):
        # [1] unresolve the issue in TMS 
        # [2] In sucess-return-response send socket-post to respective dj-service
        # print("TMSIssueUnresolveAPI class is called!")
        # print(f'ticket_issue_oid: {request.data["ticket_issue_oid"]}')
        # print(f'user_signing_token_tms: {request.data["user_signing_token_tms"]}')
        # print(f'remark_input_dismiss_value: {request.data["remark_input_dismiss_value"]}')
        # print(f'common_cso_email: {request.data["common_cso_email"]}')
        # print(f'common_registered_user_email: {request.data["common_registered_user_email"]}')
        # print(f'roomSlugParam: {request.data["roomSlugParam"]}')

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

        print("TMSIssueUnresolveAPI:", data)
        return HttpResponse("OK: 'TMSIssueUnresolveAPI' api is executed")
        # return Response(request)
        # return Response(data)

        return JsonResponse({
            'ticket_issue_oid': f'{request.data["ticket_issue_oid"]}',
            'user_signing_token_tms': f'{request.data["user_signing_token_tms"]}',
            'remark_input_dismiss_value': f'{request.data["remark_input_dismiss_value"]}',
            'common_cso_email': f'{request.data["common_cso_email"]}',
            'common_registered_user_email': f'{request.data["common_registered_user_email"]}',
            'roomSlugParam': f'{request.data["roomSlugParam"]}',
        })
    



        # return JsonResponse({
        #     'ticket_issue_oid': f'{ticket_issue_oid}',
        #     'user_signing_token_tms': f'{user_signing_token_tms}',
        #     'remark_input_resolve_value': f'{remark_input_resolve_value}',
        #     'data': "test data",
        # })
        # ticket_issue_oid = request.data['ticket_issue_oid']
        # user_signing_token_tms = request.data['user_signing_token_tms']

        # if request.data.keys() & {'ticket_issue_oid', 'user_signing_token_tms'}:
        #     data = fetch_tms_issue(ticket_issue_oid, user_signing_token_tms)

        #     return Response(data)
        # return JsonResponse({
        #     'ticket_issue_oid': f'{ticket_issue_oid}',
        #     'user_signing_token_tms': f'{user_signing_token_tms}',
        #     'data': f'{data}'
        # })
