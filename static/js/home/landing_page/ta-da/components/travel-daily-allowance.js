function TavelDailyAllowance(val) {
    gradeSelectionPrompt(tada_type=val);
}

async function tadaReportAPI(start_date, end_date, v_start_location_id, v_end_location_id, pay_grade, transport_type) {
    console.log(`tadaReportAPI() API is called!`);
    let data = {
        "start_date": `${start_date}`, 
        "end_date": `${end_date}`, 
        "v_start_location_id": `${v_start_location_id}`, 
        "v_end_location_id": `${v_end_location_id}`, 
        "pay_grade": pay_grade,
        "transport_type": "Airlines"
    }
    let apiUrl1 = `http://127.0.0.1:8080/tada-portal/calculate_ta_da/`;
    return fetch(apiUrl1, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was invalid!');
        }
        return response.json();
    })
    .then(tadaReport => {
        console.log('TA report (inside tadaReportAPI() fetch method):', tadaReport?.result);
        return tadaReport?.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function showTravelDailyAllowanceResult() {
    let tada_amount = await tadaReportAPI(tada?.start_date, tada?.end_date, tada?.start_location[0], tada?.end_location, tada?.officer_grade, tada?.transportation_type);

    
    let UserResponse_tada = `
        <p class="userMsg">
            TA/DA Calculation Report <br/>
            Officer Grade: ${tada?.officer_grade} <br/>
            Transportation Type: ${tada?.transportation_type} <br/>
            Start Date: ${tada?.start_date} <br/>
            ${startLocationReportGenerate(tada?.start_location)}
            End Location: ${tada?.end_location} <br/>
            End Date: ${tada?.end_date} <br/>
            ${tada_amount} <br/>
        </p>
        <div class="clearfix"></div>
    `;
    $(UserResponse_tada).appendTo(".chats").fadeIn(600);
    let tada_keys = Object.keys(tada);
    tada_keys.forEach(key => {
        delete tada[key];
    });
    document.querySelector("#userInput").disabled = false;
}