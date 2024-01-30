function DailyAllowance(val) {
    gradeSelectionPrompt(tada_type=val);
}

var currentDate = new Date();
var currentMonth = currentDate.getMonth();
var currentYear = currentDate.getFullYear();

function promptDate(isPromptDateDA, tada_type=null) {
    var date_heading_para = `<p class="botMsg">Please select your ${(isPromptDateDA===true) ? 'start' : 'end'} date:</p>`;
    let BotResponse_tada = `
        <img class="botAvatar" src="./static/img/sara_avatar.png"/>
        ${date_heading_para}
        <div class="clearfix"></div>
        <div class="calendar-wrapper-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}"></div>
    `;
    $(BotResponse_tada).appendTo(".chats").fadeIn(1000);
    generateCalendar(isPromptDateDA, tada_type);
}

function showDateTime(dateTinme, isPromptDateDA, tada_type=null) {
    let UserResponse_tada = `
        <p class="userMsg">${dateTinme}</p>
        <div class="clearfix"></div>
    `;
    $(UserResponse_tada).appendTo(".chats").fadeIn(600);

    if (tada_type===null) {
        if (isPromptDateDA) {
            promptDate(isPromptDateDA=false);
        }
    } else {
        if (isPromptDateDA) {
            startLocationSelectionPrompt(extra_loc=null, tada_type=tada_type, isPromptDateDA);
        } else {
            tada.end_date = dateTinme;
            showTravelDailyAllowanceResult();
        }
    }
}

function generateCalendar(isPromptDateDA, tada_type=null) {
    let calendar_wrapper = document.querySelector(`.calendar-wrapper-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);

    let calendar_container = `
        <div class="calendar-container-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}">
            <div class="calendar-header-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}">
                <i id="prevMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}" class="fa-solid fa-chevron-left"></i>
                <p id="currentMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}"></p>
                <i id="nextMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}" class="fa-solid fa-chevron-right"></i>
            </div>
        </div>
        <div class="calendar-body-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}" 
            id="calendarBody-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}"></div>
    `;

    calendar_wrapper.insertAdjacentHTML('beforeend', calendar_container);

    void calendar_wrapper.offsetWidth;
    calendar_wrapper.classList.add(`fade-in-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);

    updateCalendar(isPromptDateDA, tada_type);

    let prevMonthBtn = document.querySelector(`#prevMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
    let nextMonthBtn = document.querySelector(`#nextMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
    calendarMonthToggleButtonClick(isPromptDateDA, tada_type, prevMonthBtn, nextMonthBtn);
}

function calendarMonthToggleButtonClick(isPromptDateDA, tada_type=null, prevMonthBtn, nextMonthBtn) {
    prevMonthBtn.addEventListener("click", function () {
        currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
        currentYear = (currentMonth === 11) ? currentYear - 1 : currentYear;
        updateCalendar(isPromptDateDA, tada_type);
    });

    nextMonthBtn.addEventListener("click", function () {
        currentMonth = (currentMonth === 11) ? 0 : currentMonth + 1;
        currentYear = (currentMonth === 0) ? currentYear + 1 : currentYear;
        updateCalendar(isPromptDateDA, tada_type);
    });
}

function updateCalendar(isPromptDateDA, tada_type=null) {
    var selectedDate = null;
    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    
    var calendarBody = document.querySelector(`#calendarBody-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
    var currentMonthText = document.querySelector(`#currentMonth-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
    currentMonthText.textContent = monthNames[currentMonth] + " " + currentYear;

    var daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    var firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

    calendarBody.innerHTML = "";

    for (var i = 0; i < firstDayOfMonth; i++) {
        var emptyDay = document.createElement("div");
        emptyDay.classList.add(`empty-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
        calendarBody.appendChild(emptyDay);
    }

    for (var day = 1; day <= daysInMonth; day++) {
        var dateElement = document.createElement("div");
        dateElement.textContent = day;
        dateElement.classList.add(`day-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);

        // Click a date from calendar
        dateElement.addEventListener("click", function () {
            selectedDate = new Date(currentYear, currentMonth, parseInt(this.textContent));
            console.log("Selected Date:", selectedDate.toDateString());
            showDateTime(selectedDate.toDateString(), isPromptDateDA, tada_type);
            // Assign a 'start-date' key-value to 'tada' object
            if (isPromptDateDA) {
                tada.start_date = selectedDate.toDateString();
            } else {
                tada.end_date = selectedDate.toDateString();
                if (tada_type===null) {
                    showDailyAllowanceResult();
                }
            }
            this.classList.add(`day-selected-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
            var calendarBodyElements = document.querySelector(`#calendarBody-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`).children;
            for (var i = 0; i < calendarBodyElements.length; i++) {
                var childClass = calendarBodyElements[i].classList.value;
                if (childClass === `day day-selected-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}` 
                    && this !== calendarBodyElements[i]) {
                    calendarBodyElements[i].classList.remove(`day-selected-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
                }
            }
            let calendar_wrapper = document.querySelector(`.calendar-wrapper-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
            calendar_wrapper.classList.add(`calendar-removed-${(isPromptDateDA===true) ? 'startD_DA' : 'endD_DA'}`);
            calendar_wrapper.remove(); 
        });
        calendarBody.appendChild(dateElement);
    }
}

function dateFormatter(dateVal) {
    console.log(`dateFormatter function is called!`);
    console.log(`Start Date:`, dateVal);
    let date = new Date(dateVal);
    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString().padStart(2, '0'); 
    let day = date.getDate().toString().padStart(2, '0');
    const output = `${year}-${month}-${day}`;
    return output;
}

async function daReportAPI(start_date, end_date, pay_grade) {
    let data = {
        "start_date": `${start_date}`, 
        "end_date": `${end_date}`, 
        "pay_grade": pay_grade
    }
    let apiUrl1 = `http://127.0.0.1:8080/tada-portal/calculate_da/`;
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
        return tadaReport?.da_amount;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


async function showDailyAllowanceResult() {
    console.log('tada:', tada);
    let start_date = dateFormatter(`${tada.start_date}`);
    let end_date = dateFormatter(`${tada.end_date}`);
    let da_amount = await daReportAPI(start_date, end_date, tada.officer_grade);
    console.log('TDA report (outside daReportAPI()):', da_amount);
    
    let UserResponse_tada = `
        <p class="userMsg">
            DA Calculation Report <br/>
            Officer Grade: ${tada.officer_grade} <br/>
            Transportation Type: ${tada.transportation_type} <br/>
            Start Date: ${start_date} <br/>
            End Date: ${end_date} <br/>
            DA amount: ${da_amount} <br/>
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