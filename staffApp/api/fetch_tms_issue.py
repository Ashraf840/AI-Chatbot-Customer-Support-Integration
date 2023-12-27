from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .helper_func.tms_issue_fetch_func import fetch_tms_issue
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response


class TMSIssueDetailAPI(APIView):
    def get(self, request, ticket_issue_oid, user_signing_token_tms, format=None):
        data = fetch_tms_issue(ticket_issue_oid, user_signing_token_tms)
        return Response(data)

    def post(self, request, format=None):
        ticket_issue_oid = request.data['ticket_issue_oid']
        user_signing_token_tms = request.data['user_signing_token_tms']

        # if 'ticket_issue_oid' or 'user_signing_token_tms' in request.data:
        #     print("request-data (data):", request.data['data'])
            # pass
        if request.data.keys() & {'ticket_issue_oid', 'user_signing_token_tms'}:
            data = fetch_tms_issue(ticket_issue_oid, user_signing_token_tms)

            return Response(data)
        # return JsonResponse({
        #     'ticket_issue_oid': f'{ticket_issue_oid}',
        #     'user_signing_token_tms': f'{user_signing_token_tms}',
        #     'data': f'{data}'
        # })
