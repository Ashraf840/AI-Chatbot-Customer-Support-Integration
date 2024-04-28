function TavelAllowance(val) {
    gradeSelectionPrompt(tada_type=val);
}

function startLocationSelectionPrompt(extra_loc=null, tada_type=null, isPromptDateDA=null) {
    
    var location_heading_para = '';
    switch (extra_loc) {
        case null:
            location_heading_para = '<p class="botMsg">Please select your start location:</p>';
            break;
        case true:
            location_heading_para = '<p class="botMsg">Please select your next location:</p>';
            break;
        default:
            console.log(`Invalid extra location variable!`);
    }
    let BotResponse_tada = `
        <img class="botAvatar" src="./static/img/sara_avatar.png"/>
        ${location_heading_para}
        <select name="start_location" id="start_location" class="botMsg combobox"></select>
        <div class="clearfix"></div>`;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    let start_location = document.getElementById('start_location');
    generateLocationOptions('start_location');
    startLocationChange(start_location, extra_loc, tada_type, isPromptDateDA);
}

function startLocationChange(start_location, extra_loc, tada_type=null, isPromptDateDA=null) {
    start_location.addEventListener('click', function() {
        let startLoc = this.value;
        start_location.remove();
        let UserResponse_tada = `
            <p class="userMsg">${(extra_loc===null) ? 'Start' : 'Next'} Location: ${startLoc}</p>
            <div class="clearfix"></div>
        `;
        if (extra_loc===null) {
            tada.start_location = [startLoc];
        } else {
            tada.start_location.push(startLoc);
        }
        
        $(UserResponse_tada).appendTo(".chats").fadeIn(600);
        addStartLocationExtraPrompt(tada_type, isPromptDateDA);
    }, false);
}

function addStartLocationExtraPrompt(tada_type=null, isPromptDateDA=null) {
    let BotResponse_tada = `
        <div class="addStartLocationExtraPrompt_wrapper">
            <img class="botAvatar" src="./static/img/sara_avatar.png"/>
            <p class="botMsg">Would you like to add more location?</p>
            <div class="clearfix"></div>
            <button type="button" id="startLocExtraNo" class="tada_button btn_no" value="no">No</button>
            <button type="button" id="startLocExtraYes" class="tada_button btn_yes" value="yes">Yes</button>
        </div>
    `;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    let extraLocationPromptWrapper = document.querySelector('.addStartLocationExtraPrompt_wrapper');
    let strtLocExtraYes = document.querySelector("#startLocExtraYes");
    let strtLocExtraNo = document.querySelector("#startLocExtraNo");
    addStartLocationExtraClick(extraLocationPromptWrapper, strtLocExtraYes, strtLocExtraNo, tada_type, isPromptDateDA);
}

function EndLocation(tada_type=null, isPromptDateDA=null) {
    let BotResponse_tada = `
        <img class="botAvatar" src="./static/img/sara_avatar.png"/>
        <p class="botMsg">Please select your end location:</p>
        <select name="end_location" id="end_location" class="botMsg combobox"></select>
        <div class="clearfix"></div>
    `;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    let end_location = document.getElementById('end_location');
    generateLocationOptions('end_location');
    EndLocationChange(end_location, tada_type, isPromptDateDA);
}

function addStartLocationExtraClick(extraLocationPromptWrapper, startLocExtraYes, startLocExtraNo, tada_type=null, isPromptDateDA=null) {
    startLocExtraYes.addEventListener('click', function() {
        extraLocationPromptWrapper.remove();
        let extra_loc = true;
        startLocationSelectionPrompt(extra_loc, tada_type, isPromptDateDA);
    }, false);

    startLocExtraNo.addEventListener('click', function() {
        extraLocationPromptWrapper.remove();
        EndLocation(tada_type, isPromptDateDA);
    }, false);
}

function startLocationReportGenerate(tada_start_location) {
    let start_locations = "";

    for (i=0; i<tada_start_location.length; i++) {
        if (i===0) {
            start_locations += `Start Location: ${tada_start_location[i]} <br/>`;
        } else {
            start_locations += `Next Location: ${tada_start_location[i]} <br/>`;
        }
    }
    return start_locations;
}

function EndLocationChange(end_location, tada_type=null, isPromptDateDA=null) {
    end_location.addEventListener('click', function() {
        let endLoc = this.value;
        end_location.remove();
        let UserResponse_tada = `
            <p class="userMsg">Destination: ${endLoc}</p>
            <div class="clearfix"></div>
        `;
        tada.end_location = endLoc;
        $(UserResponse_tada).appendTo(".chats").fadeIn(600);
        
        if (tada_type===null) {
            showTravelAllowanceResult();
        } else {
            promptDate(isPromptDateDA=false, tada_type);
        }
    }, false);
}

async function taReportAPI(start_location, end_location, pay_grade, transportation_type) {
    let data = {
        "v_start_location_id": `${start_location}`, 
        "v_end_location_id": `${end_location}`, 
        "pay_grade": pay_grade,
        "transport_type": "Airlines"
    }
    let apiUrl1 = `http://127.0.0.1:8080/tada-portal/calculate_ta/`;
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
        console.log('TA report (inside taReportAPI() fetch method):', tadaReport?.ta_amount);
        return tadaReport?.ta_amount;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function showTravelAllowanceResult() {
    console.log('tada:', tada);
    let ta_amount = await taReportAPI(tada.start_location[0], tada.end_location, tada.officer_grade);
    let UserResponse_tada_report = `
        <p class="userMsg">
            TA Calculation Report <br/>
            Officer Grade: ${tada?.officer_grade} <br/>
            Transportation Type: ${tada?.transportation_type} <br/>
            ${startLocationReportGenerate(tada?.start_location)}
            End Location: ${tada?.end_location} <br/>
            TA amount: ${ta_amount} <br/>
        </p>
        <div class="clearfix"></div>
    `;
    $(UserResponse_tada_report).appendTo(".chats").fadeIn(600);

    let tada_keys = Object.keys(tada);
    tada_keys.forEach(key => {
        delete tada[key];
    });
    document.querySelector("#userInput").disabled = false;
}