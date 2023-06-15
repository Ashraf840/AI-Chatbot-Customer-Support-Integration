import requests
import json
def fetch_tms_issue(ticket_issue_oid, user_signing_token_tms):
    print("test: fetch_tms_issue")
    print("ticket_issue_oid:", ticket_issue_oid)
    print("user_signing_token_tms:", user_signing_token_tms)
    url = "http://172.16.6.134/api/v1/issue-detail-by-oid"

    payload = json.dumps({
        "oid": f"{ticket_issue_oid}"
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {user_signing_token_tms}',
        # 'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYW50aWtfbWFobXVkIiwicm9sZSI6IkNBTEwgQ0VOVEVSIEFHRU5UIiwibG9naW5fb2lkIjoiODRlYWUzMDQtZGY3Ni00MmM1LWJhNGMtODNhZTEwMGUwZjliIiwiaWF0IjoxNjg2NTcwODM5LCJleHAiOjE2ODY2NTcyMzl9.W9dMVTP7TjZBhoqMpLiosGtHRYbzQFhZ-wHUNhouya8',
        'Content-Type': 'application/json',
        'Referer': 'http://172.16.6.134/issue/admin-issue-list/6f8b28a3-0e2e-4f06-b3eb-6f7b4e2da5ac',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return response.json()
    return response.text
