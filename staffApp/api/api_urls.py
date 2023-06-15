from django.urls import path
from . import (
    fetch_tms_issue as fti,
)

app_name = "stffAppApi"

urlpatterns = [
    # tms-issue-detail-api
    # GET METHOD
    path("tms-issue/<str:ticket_issue_oid>/<user_signing_token_tms>/", fti.TMSIssueDetailAPI.as_view(), name="TMSIssueDetailAPI"),
    # POST METHOD
    path("tms-issue/", fti.TMSIssueDetailAPI.as_view(), name="TMSIssueDetailAPI"),
]
