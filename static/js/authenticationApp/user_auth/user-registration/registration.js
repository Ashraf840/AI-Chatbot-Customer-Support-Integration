function userRegistration_chatbot(data) {
    // userEmailPrompt(data);
    userRegistrationPrompt(data);
    scrollToBottomOfResults();
}


function userRegistrationPrompt(data) {
    console.log("User info:", data);
    let BotResponse_userRegistration = `
        <div class="userRegPrompt_wrapper">
            <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
            <p class="botMsg">You don't have any account regarding the phone number you've entered. Do you want to register?</p>
            <div class="clearfix"></div>
            <button type="button" id="userRegPromptNo" class="user_registration_prompt_btn btn_no" value="no">No</button>
            <button type="button" id="userRegPromptYes" class="user_registration_prompt_btn btn_yes" value="yes">Yes</button>
        </div>
    `;
    $(BotResponse_userRegistration).appendTo(".chats").fadeIn(1000);
    let userRegPromptWrapper = document.querySelector('.userRegPrompt_wrapper');
    let userRegPromptBtnYes = document.querySelector("#userRegPromptYes");
    let userRegPromptBtnNo = document.querySelector("#userRegPromptNo");
    userRegPromptClick(userRegPromptWrapper, userRegPromptBtnYes, userRegPromptBtnNo);
}


function userRegPromptClick(userRegPromptWrapper, userRegPromptBtnYes, userRegPromptBtnNo) {
    userRegPromptBtnYes.addEventListener('click', function () {
        userRegPromptWrapper.remove();
        console.log(`Redirect the user to the registration page`);
        let form = document.createElement('form');
        form.action = `/auth/user-auth/registration/`;
        form.method = 'GET';
        document.body.appendChild(form);
        form.submit();
    });

    userRegPromptBtnNo.addEventListener('click', function () {
        userRegPromptWrapper.remove();
        console.log(`Thank you!`);
        let BotResponse_userReg = `
            <div class="userRegThankYouMessage_wrapper">
                <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
                <p class="botMsg">Thank you.</p>
                <div class="clearfix"></div>
            </div>
        `;
        $(BotResponse_userReg).appendTo(".chats").fadeIn(1000);
    });
}



// // ************************ NOT GOING TO REGISTER A USER FROM THE CHATBOX UI; Going to use this after completing the login & then routing to chatroom
// function userEmailPrompt(data) {
//     let BotResponse = `
//         <div class="userEmailReg_wrapper">
//             <img class="botAvatar" src='https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg'>
//             <p class="botMsg">You don't have any account regarding the phone number you've entered. Can you please enter your email address?</p>
//             <input type="test" id="userEmailReg_input" name="userEmailReg_input" class="userEmailReg_input" placeholder="Email"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let userEmailReg_input = document.getElementById('userEmailReg_input');
//     userEmailReg_input.focus();
//     scrollToBottomOfResults();
//     userEmailRegInputKeypress(userEmailReg_input, data);
// }

// function userEmailRegInputKeypress(userEmailReg_input, data) {
//     userEmailReg_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             userEmailReg_input.remove();
//             let UserResponse = `
//                 <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//                 <p class="userMsg">Email: ${userEmailReg_input.value}</p>
//                 <div class="clearfix"></div>
//             `;
//             data['email'] = userEmailReg_input.value;
//             $(UserResponse).appendTo(".chats").fadeIn(600);
//             userPasswordPrompt(data);
//             scrollToBottomOfResults();
//         }
//     });
// }

// function userPasswordPrompt(data) {
//     let BotResponse = `
//         <div class="userPassReg_wrapper">
//             <p class="botMsg">Please enter a password.</p>
//             <input type="password" id="userPassReg_input" name="userPassReg_input" class="userPassReg_input" placeholder="Password"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let userPassReg_input = document.getElementById('userPassReg_input');
//     userPassReg_input.focus();
//     userPassRegInputKeypress(userPassReg_input, data);
//     scrollToBottomOfResults();
// }

// function userPassRegInputKeypress(userPassReg_input, data) {
//     userPassReg_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             userPassReg_input.remove();
//             let UserResponse = `
//                 <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//                 <p class="userMsg">Password: ${'*'.repeat(userPassReg_input.value.length)}</p>
//                 <div class="clearfix"></div>
//             `;
//             data['password'] = userPassReg_input.value;
//             $(UserResponse).appendTo(".chats").fadeIn(600);
//             // console.log(`user reg data:`, data);
//             userConfirmPasswordPrompt(data);
//             scrollToBottomOfResults();
//         }
//     })
// }


// function userConfirmPasswordPrompt(data) {
//     let BotResponse = `
//         <div class="userConfirmPassReg_wrapper">
//             <p class="botMsg">Please retype the password.</p>
//             <input type="password" id="userConfirmPassReg_input" name="userConfirmPassReg_input" class="userConfirmPassReg_input" placeholder="Password"><br>
//             <div class="clearfix"></div>
//         </div>
//     `;
//     $(BotResponse).appendTo(".chats").fadeIn(1000);
//     let userConfirmPassReg_input = document.getElementById('userConfirmPassReg_input');
//     userConfirmPassReg_input.focus();
//     userConfirmPassRegInputKeypress(userConfirmPassReg_input, data);
//     scrollToBottomOfResults();
// }

// function passwordMatchChecker(password, confirmPassword) {
//     return (password === confirmPassword) ? true : false;
// }

// function passwordMatchHandler(data) {
//     if (passwordMatchChecker(data?.password, data?.confirmPassword)) {
//         // <p class="userMsg">Confirm Password: ${'*'.repeat(userConfirmPassReg_input.value.length)}</p>
//         let UserResponse = `
//             <img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='>
//             <p class="userMsg">Please be patient, you'll be connected to an HDO soon!</p>
//             <div class="clearfix"></div>
//         `;
//         $(UserResponse).appendTo(".chats").fadeIn(600);
//         // *** Post data to user-reg api
//         console.log(`Post data to user-reg api!`);
//         // console.log(`user reg data:`, data);
//         // console.log(`Password:`, data?.password);
//         // console.log(`Repeat Password:`, data?.confirmPassword);
//         UserRegfromChatbotAPI(data);
//         scrollToBottomOfResults();
//     } else {
//         let BotResponse = `
//             <div class="userPassMismatchedReg_wrapper">
//                 <p class="botMsg"><span class="red-highlight">Password didn't matched</span>! Please confirm the password correctly.</p>
//                 <input type="password" id="userPassMismatchedReg_input" name="userPassMismatchedReg_input" class="userPassMismatchedReg_input" placeholder="Password"><br>
//                 <input type="password" id="userConfirmPassMismatchedReg_input" name="userConfirmPassMismatchedReg_input" class="userConfirmPassMismatchedReg_input" placeholder="Confirm Password"><br>
//                 <div class="clearfix"></div>
//             </div>
//         `;
//         $(BotResponse).appendTo(".chats").fadeIn(1000);
//         let userPassMismatchedReg_wrapper = document.querySelector('.userPassMismatchedReg_wrapper');
//         let userPassMismatchedReg_input = document.getElementById('userPassMismatchedReg_input');
//         let userConfirmPassMismatchedReg_input = document.getElementById('userConfirmPassMismatchedReg_input');
//         userPassMismatchedRegInputKeypress(
//             userPassMismatchedReg_wrapper,
//             userPassMismatchedReg_input,
//             userConfirmPassMismatchedReg_input,
//             data
//         );
//         scrollToBottomOfResults();
//     }
// }

// function userPassMismatchedRegInputKeypress(
//     userPassMismatchedReg_wrapper,
//     userPassMismatchedReg_input,
//     userConfirmPassMismatchedReg_input,
//     data
// ) {
//     console.log(`userPassMismatchedRegInputKeypress - wrapper:`, userPassMismatchedReg_wrapper);
//     userPassMismatchedReg_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             data['password'] = userPassMismatchedReg_input.value;
//             userConfirmPassMismatchedReg_input.focus();
//         }
//     });
//     userConfirmPassMismatchedReg_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             data['confirmPassword'] = userConfirmPassMismatchedReg_input.value;
//             userPassMismatchedReg_wrapper.remove();
//             passwordMatchHandler(data);
//         }
//     });
// }

// function userConfirmPassRegInputKeypress(userConfirmPassReg_input, data) {
//     userConfirmPassReg_input.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             data['confirmPassword'] = userConfirmPassReg_input.value;
//             console.log(`Password match result:`, passwordMatchChecker(data?.password, data?.confirmPassword));
//             userConfirmPassReg_input.remove();
//             passwordMatchHandler(data);
//         }
//     });
// }

// function UserRegfromChatbotAPI(data) {
//     delete data?.user_login;
//     data['user_registration'] = true;
//     let url = `http://127.0.0.1:8080/auth/user-auth/api/user-login-reg-automation/`;
//     return fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was invalid!');
//             }
//             return response.json();
//         })
//         .then(userRegReport => {
//             // console.log('userRegReport (inside UserLoginfromChatbotAPI() fetch method):', tadaReport?.ta_amount);
//             console.log('userRegReport (inside UserLoginfromChatbotAPI() fetch method):', userRegReport?.result);
//             console.log('User email:', userRegReport?.email);
//             console.log('User password:', userRegReport?.password);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// }