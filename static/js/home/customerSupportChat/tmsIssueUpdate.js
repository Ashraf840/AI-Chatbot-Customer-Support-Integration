function tmsIssueUpdate_resolve (user_signin_token, 
    remark_input_resolve_value, 
    ticket_issue_oid, 
    hdo_email_resolve_opt, 
    registered_user_email, 
    roomSlugParam) {
	console.log(`TMS Issue update opeartion is executed!`);
        console.log(`user_signin_token: ${user_signin_token}`);
        console.log(`remark_input_resolve_value: ${remark_input_resolve_value}`);
        console.log(`ticket_issue_oid: ${ticket_issue_oid}`);
        console.log(`hdo_email_resolve_opt: ${hdo_email_resolve_opt}`);
        console.log(`registered_user_email: ${registered_user_email}`);
        console.log(`roomSlugParam: ${roomSlugParam}`);
	
	const csrftoken = getCookie('csrftoken');

        console.log(`csrftoken: ${csrftoken}`);

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

	fetch(`http://${window.location.host}/staff/api/tms-issue/resolve/`, requestOptions)
        // fetch("http://ibaschat.celloscope.net/staff/api/tms-issue/resolve/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));

}




function tmsIssueUpdate_unresolve (user_signing_token_tms,
            remark_input_dismiss_value,
            ticket_issue_oid,
            common_cso_email,
            common_registered_user_email,
            roomSlugParam) {
	const csrftoken = getCookie('csrftoken');
	console.log(`tmsIssueUpdate_unresolve func is called!`);
	console.log(`csrftoken: ${csrftoken}`);
	

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

        fetch(`http://${window.location.host}/staff/api/tms-issue/unresolve/`, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));


}
