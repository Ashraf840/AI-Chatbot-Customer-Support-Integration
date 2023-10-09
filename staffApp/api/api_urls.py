from django.urls import path
from . import (
    fetch_tms_issue as fti,
    issue_resolve_func as irf,
    issue_unresolve_func as iuf,
)

app_name = "stffAppApi"

urlpatterns = [
    # tms-issue-detail-api
    # GET METHOD
    path("tms-issue/<str:ticket_issue_oid>/<user_signing_token_tms>/", fti.TMSIssueDetailAPI.as_view(), name="TMSIssueDetailAPI"),
    # POST METHOD
    path("tms-issue/", fti.TMSIssueDetailAPI.as_view(), name="TMSIssueDetailAPI"),
    # tms-issue-resolve-api
    path("tms-issue/resolve/", irf.TMSIssueResolveAPI.as_view(), name="TMSIssueResolveAPI"),
    # tms-issue-unresolve-api
    path("tms-issue/unresolve/", iuf.TMSIssueUnresolveAPI.as_view(), name="TMSIssueUnresolveAPI"),
]
