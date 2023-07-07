// TMS Issue Update: Resolve
function tmsIssueUpdate_resolve (user_signin_token, 
    remark_input_resolve_value, 
    ticket_issue_oid, 
    hdo_email_resolve_opt, 
    registered_user_email, 
    roomSlugParam) {
        console.log(`TMS Issue update opeartion is exxecuted!`);
        console.log(`user_signin_token: ${user_signin_token}`);
        console.log(`remark_input_resolve_value: ${remark_input_resolve_value}`);
        console.log(`ticket_issue_oid: ${ticket_issue_oid}`);
        console.log(`hdo_email_resolve_opt: ${hdo_email_resolve_opt}`);
        console.log(`registered_user_email: ${registered_user_email}`);
        console.log(`roomSlugParam: ${roomSlugParam}`);


        // ---------------------------------------------------------------------------------------------
        // // using jQuery
        // function getCookie(name) {
        //     var cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         var cookies = document.cookie.split(';');
        //         for (var i = 0; i < cookies.length; i++) {
        //             var cookie = jQuery.trim(cookies[i]);
        //             // Does this cookie string begin with the name we want?
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // }
        // var csrftoken = getCookie('csrftoken');
        // ---------------------------------------------------------------------------------------------

        // function getCookie(name) {
        //     let cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         const cookies = document.cookie.split(';');
        //         for (let i = 0; i < cookies.length; i++) {
        //             const cookie = cookies[i].trim();
        //             // Does this cookie string begin with the name we want?
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // }


        // function getCookie(cname) {
        //     var name = cname + "=";
        //     var decodedCookie = decodeURIComponent(document.cookie);
        //     var ca = decodedCookie.split(':');
        //     for (var i=0; i<ca.length; i++) {
        //         var c = ca[i];
        //         while (c.charAt(0) == ' ') {
        //             c = c.substring(1);
        //         }
        //         if (c.indexOf(name) == 0) {
        //             return c.substring(name.length, c.length);
        //         }
        //     }
        //     return ""
        // }
        const csrftoken = getCookie('csrftoken');

        // ----------------------------------------------------------------------


        // const options = {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: `{
        //         "ticket_issue_oid":${ticket_issue_oid},
        //         "user_signing_token_tms":${user_signin_token},
        //         "remark_input_resolve_value":${remark_input_resolve_value},
        //         "hdo_email_resolve_opt":${hdo_email_resolve_opt},
        //         "registered_user_email":${registered_user_email},
        //         "roomSlugParam":${roomSlugParam}
        //     }`
        //   };
          
        // fetch('http://127.0.0.1:8080/staff/api/tms-issue/resolve/', options)
        // .then(response => response.json())
        // .then(response => console.log(response))
        // .catch(err => console.error(err));

        // -----------------------------------------------------------------------------------
        
        

        console.log("csrf_token:", csrftoken);
        
        
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("X-CSRFToken", csrftoken);

        var raw = JSON.stringify({
            "ticket_issue_oid": `${ticket_issue_oid}`,
            "user_signing_token_tms": `${user_signin_token}`,
            "remark_input_resolve_value": `${remark_input_resolve_value}`,
            "cso_email": `${hdo_email_resolve_opt}`,
            "registered_user_email": `${registered_user_email}`,
            "roomSlugParam": `${roomSlugParam}`
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://127.0.0.1:8080/staff/api/tms-issue/resolve/", requestOptions)
        // fetch(`http://${window.location.host}/staff/api/tms-issue/resolve/`, requestOptions)
        // fetch("http://ibaschat.celloscope.net/staff/api/tms-issue/resolve/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));



        // -----------------------------------------------------------------------------------





        // var raw = JSON.stringify({
        //     "ticket_issue_oid": `${ticket_issue_oid}`,
        //     "user_signing_token_tms": `${user_signin_token}`,
        //     "remark_input_resolve_value": `${remark_input_resolve_value}`,
        //     "cso_email": `${cso_email}`,
        //     "registered_user_email": `${registered_user_email}`,
        //     "roomSlugParam": `${roomSlugParam}`
        // });

        // var get_tms_issue_detail_url = `http://${window.location.host}/staff/api/tms-issue/resolve/`;
        // console.log("tmsIssueUpdate_resolve (POST):", get_tms_issue_detail_url);

        // var requestOptions = {
        //     method: 'POST',
        //     body: raw,
        //     redirect: 'follow'
        // };

        // // fetch(`http://${window.location.host}/staff/api/tms-issue/${ticket_issue_oid}/${user_signing_token_tms}/`, requestOptions)
        // fetch(`${get_tms_issue_detail_url}`, requestOptions)
        // .then(response => response.json())
        // .then(result => {
        //     // // HIDE LOADER WILL BE IMPLEMENTED HERE
        //     // grid_tms_issue_skeleton.style.display = "none";
        //     // // grid_tms_issue_skeleton.remove();
        //     // // grid_tms_issue_data.style.visibi = "block";
        //     // grid_tms_issue_data.removeAttribute('style');

        //     console.log(result);
        // })
        // .catch(error => console.log('error', error));       // HIDE LOADER WILL BE IMPLEMENTED HERE

}










function tmsIssueUpdate_resolve_depc (user_signin_token, remark_input_resolve_value, ticket_issue_oid, cso_email, registered_user_email, roomSlugParam) {
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
                'remark_input_resolve_value': remark_input_resolve_value,
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
function tmsIssueUpdate_unresolve (user_signing_token_tms, 
            remark_input_dismiss_value, 
            ticket_issue_oid, 
            common_cso_email, 
            common_registered_user_email, 
            roomSlugParam) {
    console.log(`tmsIssueUpdate_unresolve() function is called!`);
    console.log(`user_signing_token_tms: ${user_signing_token_tms}`);
    console.log(`remark_input_dismiss_value: ${remark_input_dismiss_value}`);
    console.log(`ticket_issue_oid: ${ticket_issue_oid}`);
    console.log(`common_cso_email: ${common_cso_email}`);
    console.log(`common_registered_user_email: ${common_registered_user_email}`);
    console.log(`roomSlugParam: ${roomSlugParam}`);

    
    const csrftoken = getCookie('csrftoken');
    console.log("csrf_token:", csrftoken);


    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-CSRFToken", csrftoken);

    var raw = JSON.stringify({
        "ticket_issue_oid": `${ticket_issue_oid}`,
        "user_signing_token_tms": `${user_signing_token_tms}`,
        "remark_input_dismiss_value": `${remark_input_dismiss_value}`,
        "common_cso_email": `${common_cso_email}`,
        "common_registered_user_email": `${common_registered_user_email}`,
        "roomSlugParam": `${roomSlugParam}`
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("http://127.0.0.1:8080/staff/api/tms-issue/unresolve/", requestOptions)
    // fetch(`http://${window.location.host}/staff/api/tms-issue/unresolve/`, requestOptions)
    // fetch("http://ibaschat.celloscope.net/staff/api/tms-issue/resolve/", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));


    
    // var myHeaders = new Headers();
    // myHeaders.append("Accept", "application/json, text/plain, */*");
    // myHeaders.append("Accept-Language", "en-US,en;q=0.9");
    // myHeaders.append("Authorization", `Bearer ${user_signin_token}`);
    // myHeaders.append("Connection", "keep-alive");
    // myHeaders.append("Content-Type", "application/json");
    // myHeaders.append("Origin", "https://tms-test.celloscope.net");
    // myHeaders.append("Referer", "https://tms-test.celloscope.net/issue/96b5bddf-22da-46e5-9801-aae81844a952");
    // myHeaders.append("Sec-Fetch-Dest", "empty");
    // myHeaders.append("Sec-Fetch-Mode", "cors");
    // myHeaders.append("Sec-Fetch-Site", "same-origin");
    // myHeaders.append("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0");
    // myHeaders.append("sec-ch-ua", "\"Chromium\";v=\"112\", \"Not_A Brand\";v=\"24\", \"Opera\";v=\"98\"");
    // myHeaders.append("sec-ch-ua-mobile", "?0");
    // myHeaders.append("sec-ch-ua-platform", "\"Linux\"");

    // var raw = JSON.stringify({
    //     "remarks": `${remark_input_dismiss_value}`,
    //     "oid": `${ticket_issue_oid}`
    // });

    // var requestOptions = {
    //     method: 'POST',
    //     headers: myHeaders,
    //     body: raw,
    //     redirect: 'follow'
    // };

    // fetch("http://172.16.6.134/api/v1/update-issue-status-by-oid", requestOptions)
    // .then(response => response.json())
    // .then(result => {
    //     console.log(result);
    //     if (result?.message === "Status has been updated") {
    //         console.log('Status is updated (dismissed/ready to assign)!');
    //         ChatSupportSocket.send(JSON.stringify({
    //             'cso_user_convo_dismissed': 'CSO has dismissed the chat!',
    //             'remark_input_dismiss_value': remark_input_dismiss_value,
    //             'cso_email': common_cso_email,
    //             'reg_user_email': common_registered_user_email,
    //             'roomslug': roomSlugParam,
    //         }));
    //     } else {
    //         console.log('Invalid!');
    //     }
    // })
    // .catch(error => console.log('error', error));




}