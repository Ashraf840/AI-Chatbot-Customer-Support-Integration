function generateOptions(start, end) {
    let options = "";
    for (let i = start; i <= end; i++) {
        options += `<option value="${i}">${i}</option>`;
    }
    return options;
}

function tadaCalculationHeader(tada_type) {
    let header = "";
    switch (tada_type) {
        case 'ta':
            header += `<h5 class="tada_calc_header">TA Calculation</h5>`;
            break;
        case 'da':
            header += `<h5 class="tada_calc_header">DA Calculation</h5>`;
            break;
        case 'tada':
            header += `<h5 class="tada_calc_header">TA/DA Calculation</h5>`;
            break;
        default:
            console.log(`TA/DA calculation header: Invalid tada type!`);
    }
    return header;
}

function gradeSelectionPrompt(tada_type=null) {
    let BotResponse_tada = `
        ${tadaCalculationHeader(tada_type)}
        <img class="botAvatar" src="./static/img/sara_avatar.png"/>
        <p class="botMsg">Please select your grade:</p>
        <select name="officer_grade" id="officer_grade" class="botMsg combobox">
            ${generateOptions(1, 20)}
        </select>
        <div class="clearfix"></div>
    `;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    let selected_grade = document.getElementById('officer_grade');
    switch (tada_type) {
        case 'ta':
            officeGradeSelect(selected_grade, tada_type);
            break;
        case 'da':
            officeGradeSelect(selected_grade, tada_type);
            break;
        case 'tada':
            officeGradeSelect(selected_grade, tada_type);
            break;
        default:
            console.log("Invalid tada type:", tada_type);
    }
}

function generateLocationOptions(location) {
    switch (location) {
        case 'start_location':
            let apiUrl_startLoc = `http://127.0.0.1:8080/tada-portal/get-location-list/?location_state=start_location&language=bn`;
            let start_loc_select = document.querySelector('#start_location');
            console.log(`Invoke start_location api!`);
            fetch(apiUrl_startLoc)
                .then(response => response.json())
                .then(data => {
                    for (let i=0; i<data?.start_locations.length; i++) {
                        let option = document.createElement('option');
                        option.value = data?.start_locations[i]?.start_location_id;
                        option.textContent = data?.start_locations[i]?.start_location_name_bn;
                        
                        start_loc_select.appendChild(option);
                    }
                })
                .catch(error => console.error('Error:', error));
            break;
        case 'end_location':
            let apiUrl_endLoc = `http://127.0.0.1:8080/tada-portal/get-location-list/?location_state=end_location&language=bn`;
            let end_loc_select = document.querySelector('#end_location');
            console.log(`Invoke end_location api!`);

            fetch(apiUrl_endLoc)
                .then(response => response.json())
                .then(data => {
                    for (let i=0; i<data?.end_locations.length; i++) {
                        let option = document.createElement('option');
                        option.value = data?.end_locations[i]?.end_location_id;
                        option.textContent = data?.end_locations[i]?.end_location_name_bn;
                        
                        end_loc_select.appendChild(option);
                    }
                })
                .catch(error => console.error('Error:', error));
            break;
        default:
            console.log(`Invalid location option!`);
    }

    let locations = ["Dhaka", "Chittagong", "Rajshahi", "Khulna","Barisal", "Sylhet", "Rangpur", "Cox's Bazar"];
    return generateOptionsFromArray(locations, option='location');
}

function generateTransporationType() {
    let transporationTypes = ["By Air", "By Road"];
    return generateOptionsFromArray(transporationTypes, option='transportationType');
}

function generateOptionsFromArray(optionsArray, option=null) {
    let options = "";
    switch (option) {
        case 'location':
            for (let option of optionsArray) {
                options += `<option value="${option}">${option}</option>`;
            }
            break;
        case 'transportationType':
            for (let option of optionsArray) {
                options += `<option value="${option.toLowerCase()}">${option}</option>`;
            }
        break;
        default:
            console.log(`Invalid option!`);
    }
    
    return options;
}

function transportationTypeSelectionPrompt(tada_type) {
    generateTransporationType();
    let BotResponse_tada = `
        <img class="botAvatar" src="./static/img/sara_avatar.png"/>
        <p class="botMsg">Please select your transporation type:</p>
        <select name="transportation_type" id="transportation_type" class="botMsg combobox">
            ${generateTransporationType()}
        </select>
        <div class="clearfix"></div>
    `;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    let transportation = document.getElementById('transportation_type');
    transportationTypeSelect(transportation, tada_type);
}

function transportationTypeSelect(transportation, tada_type) {
    transportation.addEventListener('click', function() {
        let transportation_type = this.value;
        tada.transportation_type = transportation_type;
        transportation.remove();
        let UserResponse_tada = `
            <p class="userMsg">Transportation Type: ${transportation_type}</p>
            <div class="clearfix"></div>
        `;
        $(UserResponse_tada).appendTo(".chats").fadeIn(600);
        promptModuleRouting(tada_type);
    });
}

function officeGradeSelect(grade, tada_type) {
    grade.addEventListener('click', function() {
        let officer_grade = this.value;
        tada.officer_grade = officer_grade;
        grade.remove();
        let UserResponse_tada = `
            <p class="userMsg">Officer Grade: ${officer_grade}</p>
            <div class="clearfix"></div>
        `;
        $(UserResponse_tada).appendTo(".chats").fadeIn(600);
        if (officer_grade >=1 && officer_grade <=5) {
            transportationTypeSelectionPrompt(tada_type);
        } else {
            tada.transportation_type = 'by road';
            promptModuleRouting(tada_type);
        }
    }, false);
}

function promptModuleRouting(tada_type) {
    switch (tada_type) {
        case 'ta':
            tada.type = 'Travel Allowance';
            console.log(`Grade selection for TA module!`);
            startLocationSelectionPrompt();
            break;
        case 'da':
            tada.type = 'Daily Allowance';
            console.log(`Grade selection for DA module!`);
            promptDate(isPromptDateDA=true, tada_type=null);
            break;
        case 'tada':
            tada.type = 'Travel Daily Allowance';
            console.log(`Grade selection for TA/DA module!`);
            promptDate(isPromptDateDA=true, tada_type='tada');
            break;
    }
}