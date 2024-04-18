function userLogin() {
    let data = {};
    console.log(`User login module will be executed`);
    document.querySelector("#user-input").disabled = true;  // Disable user Input while running the user-login module
    userNIDPrompt(data);
}

function userNIDPrompt(data) {
    let BotResponse = `
        <div class="userNid_wrapper">
            <p class="botMsg">Please enter you NID number.</p>
            <input type="test" id="nidNum_input" name="nidNum_input" class="nidNum_input" placeholder="NID Number"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let nidNum_input = document.getElementById('nidNum_input');
    nidNum_input.focus();
    nidNumInputKeypress(nidNum_input, data);
    scrollToBottomOfResults();
}

function nidNumInputKeypress(nidNum_input, data) {
    nidNum_input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            nidNum_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">NID: ${nidNum_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['nid_num'] = nidNum_input.value;
            $(UserResponse).appendTo(".chats").fadeIn(600);
            userMobilePrompt(data);
            scrollToBottomOfResults();
        }
    });
}

function userMobilePrompt(data) {
    let BotResponse = `
        <div class="userMobile_wrapper">
            <p class="botMsg">Please enter you mobile number.</p>
            <input type="test" id="phone_input" name="phone_input" class="phone_input" placeholder="Mobile Number"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let phone_input = document.getElementById('phone_input');
    phone_input.focus();
    mobileNumInputKeypress(phone_input, data);
    scrollToBottomOfResults();
}

function mobileNumInputKeypress(phone_input, data) {
    phone_input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            phone_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">Mobile: ${phone_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['phone'] = phone_input.value;
            $(UserResponse).appendTo(".chats").fadeIn(600);
            userDistrictPrompt(data);
            scrollToBottomOfResults();
        }
    });
}

function userDistrictPrompt(data) {
    let BotResponse = `
        <div class="userDistrict_wrapper">
            <p class="botMsg">Please enter you district name.</p>
            <input type="test" id="districtName_input" name="districtName_input" class="districtName_input" placeholder="District"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let districtName_input = document.getElementById('districtName_input');
    districtName_input.focus();
    districtNameInputKeypress(districtName_input, data);
    scrollToBottomOfResults();
}

function districtNameInputKeypress(districtName_input, data) {
    districtName_input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            districtName_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">District: ${districtName_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['district_name'] = districtName_input.value;
            $(UserResponse).appendTo(".chats").fadeIn(600);
            
            userQueryPrompt(data);
            
            scrollToBottomOfResults();
        }
    });
}

// NB: Here's it's getting funnier, when the user has to input the same query just to connect to the HDO. If I don't ask it using the following JS function, then the ML engineer (@zubair) has to make some tweaking in the actions.py file in the chatbot codebase so that the chatbot dispatches the user-auth-related texts along with the issue descriptions.
// Although it's funny & required to be changed in later version, currently for the sake of pitching the tender, I'm taking the user query here as well.
// Moreover, this specific new requirement is also provided by the iBAS++ team.

function userQueryPrompt(data) {
    let BotResponse = `
        <div class="userQuery_wrapper">
            <p class="botMsg">Please write your query to HDO.</p>
            <input type="test" id="userQuery_input" name="userQuery_input" class="userQuery_input" placeholder="Query"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let userQuery_input = document.getElementById('userQuery_input');
    userQuery_input.focus();
    userQueryInputKeypress(userQuery_input, data);
    scrollToBottomOfResults();
}

function userQueryInputKeypress(userQuery_input, data) {
    userQuery_input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            userQuery_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">Query: ${userQuery_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['user_query'] = userQuery_input.value;
            console.log(`User input data before auth:`, data);
            $(UserResponse).appendTo(".chats").fadeIn(600);
            // Call the login-checker-api
            console.log(`Call the login-checker-api`);
            UserLoginfromChatbotAPI(data);
            scrollToBottomOfResults();
        }
    });
}

function UserLoginfromChatbotAPI(data) {
    data['user_login'] = true;
    let url = `http://127.0.0.1:8080/auth/user-auth/api/user-login-reg-automation/`;
    return fetch(url, {
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
        .then(userLoginReport => {
            // console.log('userLoginReport (inside UserLoginfromChatbotAPI() fetch method):', tadaReport?.ta_amount);
            console.log('userLoginReport (inside UserLoginfromChatbotAPI() fetch method):', userLoginReport?.result);
            if (userLoginReport?.result === "User account exists") {
                console.log(`User is registered!`);
                console.log(`Activate user login module`);  // Will hit this same API.
            }
            if (userLoginReport?.result === "User account doesn't exist!") {
                console.log(`User is unregistered!`);
                console.log(`Activate user registration module`);
                userRegistration_chatbot(data);
            }
            return userLoginReport?.result;
        })
        .catch(error => {
            console.error('Error:', error);
    });
}
