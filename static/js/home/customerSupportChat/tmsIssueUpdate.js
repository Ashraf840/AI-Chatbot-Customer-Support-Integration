// TMS Issue Update: Resolve
function tmsIssueUpdate_resolve (user_signin_token, remark_input_resolve_value, ticket_issue_oid, cso_email, registered_user_email, roomSlugParam) {
    // console.log(`tmsIssueUpdate_resolve() function is called!`);
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json, text/plain, */*");
    myHeaders.append("Authorization", `Bearer ${user_signin_token}`);
    myHeaders.append("Content-Type", "application/json");
    // myHeaders.append("Referer", "https://tms-test.celloscope.net/issue/97ebbd9a-8faf-41c1-99fd-9496b7f5c8fa");
    myHeaders.append("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36");
    myHeaders.append("sec-ch-ua", "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"");
    myHeaders.append("sec-ch-ua-mobile", "?0");
    myHeaders.append("sec-ch-ua-platform", "\"Linux\"");

    var raw = JSON.stringify({
        "remarks": `${remark_input_resolve_value}`,
        // "remarks": `sdfoiudsfoiu`,
        "issueOid": `${ticket_issue_oid}`
        // "issueOid": `5f50b242-00f9-4728-aabd-223dacca9f68`
        // "issueOid": `cfe5ac26-cd9e-4dd5-9908-307b520582cc`
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    // fetch("https://tms-test.celloscope.net/api/v1/issue-resolve-by-call-center-agent", requestOptions)
    fetch("http://172.16.6.134/api/v1/issue-resolve-by-call-center-agent", requestOptions)
    // .then(response => response.text())
    .then(response => response.json())
    // .then(result => console.log(result))
    .then(result => {
        console.log(result);
        // console.log(result?.message);
        if (result?.message === "Status has been updated") {
            console.log('Status is updated (resolved)!');
            ChatSupportSocket.send(JSON.stringify({
                'support_is_resolved': 'The support is resolved!',
                'cso_email': cso_email,
                'reg_user_email': registered_user_email,
                'roomslug': roomSlugParam
            }));
        } else {
            console.log('Invalid!');
        }
    })
    .catch(error => console.log('error', error));
}

// TMS Issue Update: Unsolved/Dismiss/Send to team lead/Ready to assign
function tmsIssueUpdate_unresolve (user_signin_token, remark_input_dismiss_value, ticket_issue_oid, common_cso_email, common_registered_user_email, roomSlugParam) {
    console.log(`tmsIssueUpdate_unresolve() function is called!`);
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json, text/plain, */*");
    myHeaders.append("Accept-Language", "en-US,en;q=0.9");
    myHeaders.append("Authorization", `Bearer ${user_signin_token}`);
    myHeaders.append("Connection", "keep-alive");
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Origin", "https://tms-test.celloscope.net");
    myHeaders.append("Referer", "https://tms-test.celloscope.net/issue/96b5bddf-22da-46e5-9801-aae81844a952");
    myHeaders.append("Sec-Fetch-Dest", "empty");
    myHeaders.append("Sec-Fetch-Mode", "cors");
    myHeaders.append("Sec-Fetch-Site", "same-origin");
    myHeaders.append("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0");
    myHeaders.append("sec-ch-ua", "\"Chromium\";v=\"112\", \"Not_A Brand\";v=\"24\", \"Opera\";v=\"98\"");
    myHeaders.append("sec-ch-ua-mobile", "?0");
    myHeaders.append("sec-ch-ua-platform", "\"Linux\"");

    var raw = JSON.stringify({
        "remarks": `${remark_input_dismiss_value}`,
        "oid": `${ticket_issue_oid}`
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://172.16.6.134/api/v1/update-issue-status-by-oid", requestOptions)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result?.message === "Status has been updated") {
            console.log('Status is updated (dismissed/ready to assign)!');
            ChatSupportSocket.send(JSON.stringify({
                'cso_user_convo_dismissed': 'CSO has dismissed the chat!',
                'cso_email': common_cso_email,
                'reg_user_email': common_registered_user_email,
                'roomslug': roomSlugParam,
            }));
        } else {
            console.log('Invalid!');
        }
    })
    .catch(error => console.log('error', error));
}