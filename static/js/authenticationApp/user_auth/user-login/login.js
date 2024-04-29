function userLogin(issue_desc) {
    let data = { issue_desc: issue_desc };
    console.log(`User login module will be executed`);
    document.querySelector("#user-input").disabled = true;  // Disable user Input while running the user-login module
    // userNIDPrompt(data);    // NOT USING IN THE LOGIN WORKFLOW

    userMobileLoginPrompt(data);
    scrollToBottomOfResults();
}

// function userNIDPrompt(data) {
//     console.log("NID stage - data:", data);
//     let BotResponse = `
//         <div class="userNid_wrapper">
//             <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
//             <p class="botMsg">Please enter you NID number.</p>
//             <input type="test" id="nidNum_input" name="nidNum_input" class="nidNum_input" placeholder="NID Number"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let nidNum_input = document.getElementById('nidNum_input');
//     nidNum_input.focus();
//     nidNumInputKeypress(nidNum_input, data);
//     scrollToBottomOfResults();
// }

// function nidNumInputKeypress(nidNum_input, data) {
//     nidNum_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             nidNum_input.remove();
//             let UserResponse = `
//                 <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//                 <p class="userMsg">NID: ${nidNum_input.value}</p>
//                 <div class="clearfix"></div>
//             `;
//             data['nid_num'] = nidNum_input.value;
//             $(UserResponse).appendTo(".chats").fadeIn(600);
//             userMobilePrompt(data);
//             scrollToBottomOfResults();
//         }
//     });
// }

function userMobileLoginPrompt(data) {
    let BotResponse = `
        <div class="userMobileLogin_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
            <p class="botMsg">Please enter you mobile number.</p>
            <input type="text" id="phone_input" name="phone_input" class="phone_input" value="01917739840" placeholder="01917739840"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let phone_input = document.getElementById('phone_input');
    phone_input.focus();
    loginMobileNumInputKeypress(phone_input, data);
    scrollToBottomOfResults();
}

function loginMobileNumInputKeypress(phone_input, data) {
    phone_input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            phone_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">Mobile: ${phone_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['phone'] = phone_input.value;
            $(UserResponse).appendTo(".chats").fadeIn(600);
            // userDistrictPrompt(data);    // NOT USING IN THE LOGIN WORKFLOW
            UserLoginfromChatbotAPI(data);
            scrollToBottomOfResults();
        }
    });
}

// NOT USING IN THE LOGIN WORKFLOW
// function userDistrictPrompt(data) {
//     let BotResponse = `
//         <div class="userDistrict_wrapper">
//             <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
//             <p class="botMsg">Please enter you district name.</p>
//             <input type="test" id="districtName_input" name="districtName_input" class="districtName_input" placeholder="District"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let districtName_input = document.getElementById('districtName_input');
//     districtName_input.focus();
//     districtNameInputKeypress(districtName_input, data);
//     scrollToBottomOfResults();
// }

// function districtNameInputKeypress(districtName_input, data) {
//     districtName_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             districtName_input.remove();
//             let UserResponse = `
//                 <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//                 <p class="userMsg">District: ${districtName_input.value}</p>
//                 <div class="clearfix"></div>
//             `;
//             data['district_name'] = districtName_input.value;
//             $(UserResponse).appendTo(".chats").fadeIn(600);

//             userQueryPrompt(data);

//             scrollToBottomOfResults();
//         }
//     });
// }

// // NB: Here's it's getting funnier, when the user has to input the same query just to connect to the HDO. If I don't ask it using the following JS function, then the ML engineer (@zubair) has to make some tweaking in the actions.py file in the chatbot codebase so that the chatbot dispatches the user-auth-related texts along with the issue descriptions.
// // Although it's funny & required to be changed in later version, currently for the sake of pitching the tender, I'm taking the user query here as well.
// // Moreover, this specific new requirement is also provided by the iBAS++ team.

// function userQueryPrompt(data) {
//     let BotResponse = `
//         <div class="userQuery_wrapper">
//             <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
//             <p class="botMsg">Please write your query to HDO.</p>
//             <input type="test" id="userQuery_input" name="userQuery_input" class="userQuery_input" placeholder="Query"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let userQuery_input = document.getElementById('userQuery_input');
//     userQuery_input.focus();
//     userQueryInputKeypress(userQuery_input, data);
//     scrollToBottomOfResults();
// }

// function userQueryInputKeypress(userQuery_input, data) {
//     userQuery_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             userQuery_input.remove();
//             let UserResponse = `
//                 <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//                 <p class="userMsg">Query: ${userQuery_input.value}</p>
//                 <div class="clearfix"></div>
//             `;
//             data['user_query'] = userQuery_input.value;
//             console.log(`User input data before auth:`, data);
//             $(UserResponse).appendTo(".chats").fadeIn(600);
//             // Call the login-checker-api
//             console.log(`Call the login-checker-api`);
//             UserLoginfromChatbotAPI(data);
//             scrollToBottomOfResults();
//         }
//     });
// }

function userLoginPrompt(phone, issue_desc) {
    // console.log("Ask user if s/he wants to login in order to communicate with the HDO!")
    let BotResponse_userLoginPrompt = `
        <div class="userLoginPrompt_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
            <p class="botMsg">We have found an account with the phone number ${phone}. Do you want to login?</p>
            <div class="clearfix"></div>
            <button type="button" id="userLoginPromptBtnNo" class="user_login_prompt_btn btn_no" value="no">No</button>
            <button type="button" id="userLoginPromptBtnYes" class="user_login_prompt_btn btn_yes" value="yes">Yes</button>
        </div>
    `;
    $(BotResponse_userLoginPrompt).appendTo(".chats").fadeIn(1000);
    let userLoginPrompt_wrapper = document.querySelector('.userLoginPrompt_wrapper');
    let userLoginPromptBtnYes = document.querySelector("#userLoginPromptBtnYes");
    let userLoginPromptBtnNo = document.querySelector("#userLoginPromptBtnNo");
    userLoginPromptClick(userLoginPrompt_wrapper, userLoginPromptBtnYes, userLoginPromptBtnNo, issue_desc);
}

function userLoginPromptClick(userLoginPrompt_wrapper, userLoginPromptBtnYes, userLoginPromptBtnNo, issue_desc) {
    userLoginPromptBtnYes.addEventListener('click', function () {
        userLoginPrompt_wrapper.remove();
        // console.log(`Ask for email & then password!`);
        userEmailLoginPrompt(issue_desc);
        scrollToBottomOfResults();
    });

    userLoginPromptBtnNo.addEventListener('click', function () {
        userLoginPrompt_wrapper.remove();
        let BotResponse_userLogin = `
            <div class="userLoginPromptInfo_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
                <p class="botMsg">You need to login to connect with an HDO. Thank you.</p>
                <div class="clearfix"></div>
            </div>
        `;
        $(BotResponse_userLogin).appendTo(".chats").fadeIn(1000);
        document.querySelector("#user-input").disabled = false;
    });
}

function userEmailLoginPrompt(issue_desc) {
    // // Since exisitng user is found now let's authenticate the user in the forntend form submission
    // let data = {};
    let data = { issue_desc: issue_desc };
    let BotResponse = `
        <div class="userEmailLogin_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
            <p class="botMsg">Please enter you email.</p>
            <input type="text" id="email_input" name="email_input" class="email_input" value="tanjim.ashraf@gmail.com" placeholder="tanjim.ashraf@gmail.com"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let email_input = document.getElementById('email_input');
    email_input.focus();
    userEmailLoginInputKeypress(email_input, data)
    scrollToBottomOfResults();
}

function userEmailLoginInputKeypress(userEmailLogin_input, data) {
    userEmailLogin_input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            userEmailLogin_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">Email: ${userEmailLogin_input.value}</p>
                <div class="clearfix"></div>
            `;
            data['email'] = userEmailLogin_input.value;
            console.log("user email for login:", data['email']);
            $(UserResponse).appendTo(".chats").fadeIn(600);
            userLoginPasswordPrompt(data);
            scrollToBottomOfResults();
        }
    });
}

function userLoginPasswordPrompt(data) {
    let BotResponse = `
        <div class="userPassLogin_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
            <p class="botMsg">Please enter a password.</p>
            <input type="password" id="userPassLogin_input" name="userPassLogin_input" class="userPassLogin_input" value="dcba4321" placeholder="dcba4321"><br>
            <div class="clearfix"></div>
        </div>
    `;
    $(BotResponse).appendTo(".chats").fadeIn(1000);
    let userPassLogin_input = document.getElementById('userPassLogin_input');
    userPassLogin_input.focus();
    userPassLoginInputKeypress(userPassLogin_input, data);
    scrollToBottomOfResults();
}

function submitLoginForm(data) {
    console.log(`user login data - email:`, data?.email);
    console.log(`user login data - password:`, data?.password);
    console.log("issue_desc - login() method", data?.issue_desc);

    let form = document.createElement('form');
    form.action = `#`;
    form.method = 'POST';
    form.style.display = 'none';

    let input_email = document.createElement('input');
    input_email.type = 'email';
    input_email.name = 'email';
    input_email.value = data?.email;
    form.appendChild(input_email);

    let input_password = document.createElement('input');
    input_password.type = 'password';
    input_password.name = 'password';
    input_password.value = data?.password;
    form.appendChild(input_password);

    let input_issue_desc = document.createElement('input');
    input_issue_desc.type = 'text';
    input_issue_desc.name = 'issue_desc';
    input_issue_desc.value = data?.issue_desc;
    form.appendChild(input_issue_desc);

    const csrftoken = getCookie('csrftoken');
    let csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrftoken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
}

function userPassLoginInputKeypress(userPassLogin_input, data) {
    userPassLogin_input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            userPassLogin_input.remove();
            let UserResponse = `
                <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
                <p class="userMsg">Password: ${'*'.repeat(userPassLogin_input.value.length)}</p>
                <div class="clearfix"></div>
            `;
            data['password'] = userPassLogin_input.value;
            $(UserResponse).appendTo(".chats").fadeIn(600);
            console.log(`user login data:`, data);
            submitLoginForm(data);
        }
    })
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
                userLoginPrompt(userLoginReport?.phone, data?.issue_desc);
                scrollToBottomOfResults();
            }
            if (userLoginReport?.result === "User account doesn't exist!") {
                console.log(`User is unregistered!`);
                console.log(`Activate user registration module`);
                userRegistration_chatbot(data);
                scrollToBottomOfResults();
            }
            return userLoginReport?.result;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
