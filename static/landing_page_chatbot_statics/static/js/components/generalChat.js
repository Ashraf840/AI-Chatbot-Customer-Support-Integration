`{% load static %}`

/**
 * scroll to the bottom of the chats after new message has been added to chat
 */
const converter = new showdown.Converter();
function scrollToBottomOfResults() {
    const terminalResultsDiv = document.getElementById("chats");
    terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}


/**
 * Set user response on the chat screen
 * @param {String} message user message
 */
function setUserResponse(message) {
    console.log(`setUserResponse - message:`, message);
    const user_response_gen = `<img class="userAvatar" src='https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='><p class="userMsg">${message} </p><div class="clearfix"></div>`;
    $(user_response_gen).appendTo(".chats").show("slow");

    $(".usrInput").val("");
    scrollToBottomOfResults();
    showBotTyping();
    $(".suggestions").remove();
}


/**
 * returns formatted bot response 
 * @param {String} text bot message response's text
 *
 */
function getBotResponse(text) {
    botResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><span class="botMsg">${text}</span><div class="clearfix"></div>`;
    return botResponse;
}

function hdoConnectionPrompt(suggestionButtons) {
    let BotResponse_hdoConnection = `
        <div class="hdoConnectionPrompt_wrapper">
            <div class="clearfix"></div>
            <button type="button" id="hdoConnectionPromptNo" class="hdo_connection_prompt_btn btn_no" value="no">No</button>
            <button type="button" id="hdoConnectionPromptYes" class="hdo_connection_prompt_btn btn_yes" value="yes">Yes</button>
        </div>
    `;
    $(BotResponse_hdoConnection).appendTo(".chats").fadeIn(1000);
    let hdoConnectionPromptWrapper = document.querySelector('.hdoConnectionPrompt_wrapper');
    let hdoConnectionPromptBtnYes = document.querySelector("#hdoConnectionPromptYes");
    let hdoConnectionPromptBtnNo = document.querySelector("#hdoConnectionPromptNo");
    hdoConnectionPromptClick(hdoConnectionPromptWrapper, hdoConnectionPromptBtnYes, hdoConnectionPromptBtnNo, suggestionButtons);
}

function hdoConnectionPromptClick(hdoConnectionPromptWrapper, hdoConnectionPromptBtnYes, hdoConnectionPromptBtnNo, suggestionButtons) {
    hdoConnectionPromptBtnYes.addEventListener('click', function() {
        hdoConnectionPromptWrapper.remove();
        console.log(`Ask for login credentials followed by showing the suggestion buttons!`);
        addSuggestion(suggestionButtons);
    });

    hdoConnectionPromptBtnNo.addEventListener('click', function() {
        hdoConnectionPromptWrapper.remove();
        console.log(`Thank you!`);
        let BotResponse_hdoConnection = `
            <div class="hdoConnectionThankYouMessage_wrapper">
                <p class="botMsg">Thank you.</p>
                <div class="clearfix"></div>
            </div>
        `;
        $(BotResponse_hdoConnection).appendTo(".chats").fadeIn(1000);
    });
}

/**
 * renders bot response on to the chat screen
 * @param {Array} response json array containing different types of bot response
 *
 * for more info: `https://rasa.com/docs/rasa/connectors/your-own-website#request-and-response-format`
 */
function setBotResponse(response) {
    setTimeout(() => {
        hideBotTyping(); 
        if (response_status=="success" && response.length < 1 ){
            const fallbackMsg = "দুঃখিত কোনো ধরনের সমস্যা হয়েছে, পুনরায় চেষ্টা করুন";
            const BotResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${fallbackMsg}</p><div class="clearfix"></div>`;

            $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
            scrollToBottomOfResults();
        }
        else if(response_status=="success"){
            // if we get response from Rasa
            for (let i = 0; i < response.length; i += 1) {
                // check if the response contains "text"
                if (Object.hasOwnProperty.call(response[i], "text")) {
                    if (response[i].text != null) {
                        // convert the text to mardown format using showdown.js(https://github.com/showdownjs/showdown);
                        let botResponse;
                        let html = converter.makeHtml(response[i].text);
                        html = html.replaceAll("<p>", "").replaceAll("</p>", "").replaceAll("<strong>", "<b>").replaceAll("</strong>", "</b>");
                        html = html.replace(/(?:\r\n|\r|\n)/g, '<br>')
                        console.log(html);
                        // check for blockquotes
                        if (html.includes("<blockquote>")) {
                            html = html.replaceAll("<br>", "");
                            botResponse = getBotResponse(html);
                        }
                        // check for image
                        if (html.includes("<img")) {
                            html = html.replaceAll("<img", '<img class="imgcard_mrkdwn" ');
                            botResponse = getBotResponse(html);
                        }
                        // check for preformatted text
                        if (html.includes("<pre") || html.includes("<code>")) {
                            botResponse = getBotResponse(html);
                        }
                        // check for list text
                        if (html.includes("<ul") || html.includes("<ol") || html.includes("<li") || html.includes('<h3')) {
                            html = html.replaceAll("<br>", "");
                            botResponse = getBotResponse(html);
                        }
                        else {
                            // if no markdown formatting found, render the text as it is.
                            if (!botResponse) {
                                if (response[i].text === "daily_allowance"
                                    || response[i].text === "travel_allowance"
                                    || response[i].text === "travel_and_daily_allowance"
                                ) {
                                    console.log(`Don't show the TADA related text!`);
                                    return;
                                }
                                if (response[i].text === "দয়া করে প্রথমে লগ ইন করুন।"
                                    || response[i].text === "Please login first."
                                ) {
                                    // console.log(`Activate user login module!`);
                                    userLogin();
                                    return;
                                }
                                if (response[i].text === "ব্যবহারকারী লগ ইন অবস্থায়ে অছেন।"
                                    || response[i].text === "User is logged in."
                                ) {
                                    console.log(`Activate issue creation & chatroom redirection module!`);
                                    return;
                                }
                                botResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${response[i].text}</p><div class="clearfix"></div>`;
                            }
                        }
                        // append the bot response on to the chat screen
                        $(botResponse).appendTo(".chats").hide().fadeIn(1000);
                    }
                }

                // check if the response contains "images"
                if (Object.hasOwnProperty.call(response[i], "image")) {
                    if (response[i].image !== null) {
                        const BotResponse = `<div class="singleCard"><img class="imgcard" src="${response[i].image}"></div><div class="clearfix">`;

                        $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
                    }
                }

                // check if the response contains "buttons"
                if (Object.hasOwnProperty.call(response[i], "buttons")) {
                    if (response[i].buttons.length > 0) {
                        hdoConnectionPrompt(response[i].buttons);
                        // addSuggestion(response[i].buttons);  // after clicking "yes" or "no" button of HdoConnectionPrompt() func, if clicked "yes", then show the suggestionButtons.
                    }
                }

                // check if the response contains "attachment"
                if (Object.hasOwnProperty.call(response[i], "attachment")) {
                    if (response[i].attachment != null) {
                        if (response[i].attachment.type === "video") {
                            // check if the attachment type is "video"
                            const video_url = response[i].attachment.payload.src;

                            const BotResponse = `<div class="video-container"> <iframe src="${video_url}" frameborder="0" allowfullscreen></iframe> </div>`;
                            $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
                        }
                    }
                }
                // check if the response contains "custom" message
                if (Object.hasOwnProperty.call(response[i], "custom")) {
                    const { payload } = response[i].custom;
                    if (payload === "quickReplies") {
                        // check if the custom payload type is "quickReplies"
                        const quickRepliesData = response[i].custom.data;
                        showQuickReplies(quickRepliesData);
                        return;
                    }

                    // check if the custom payload type is "pdf_attachment"
                    if (payload === "pdf_attachment") {
                        renderPdfAttachment(response[i]);
                        return;
                    }

                    // check if the custom payload type is "dropDown"
                    if (payload === "dropDown") {
                        const dropDownData = response[i].custom.data;
                        renderDropDwon(dropDownData);
                        return;
                    }

                    // check if the custom payload type is "location"
                    if (payload === "location") {
                        $("#userInput").prop("disabled", true);
                        getLocation();
                        scrollToBottomOfResults();
                        return;
                    }

                    // check if the custom payload type is "cardsCarousel"
                    if (payload === "cardsCarousel") {
                        const restaurantsData = response[i].custom.data;
                        showCardsCarousel(restaurantsData);
                        return;
                    }

                    // check if the custom payload type is "chart"
                    if (payload === "chart") {
                        /**
                         * sample format of the charts data:
                         *  var chartData =  { "title": "Leaves", "labels": ["Sick Leave", "Casual Leave", "Earned Leave", "Flexi Leave"], "backgroundColor": ["#36a2eb", "#ffcd56", "#ff6384", "#009688", "#c45850"], "chartsData": [5, 10, 22, 3], "chartType": "pie", "displayLegend": "true" }
                         */

                        const chartData = response[i].custom.data;
                        const {
                            title,
                            labels,
                            backgroundColor,
                            chartsData,
                            chartType,
                            displayLegend,
                        } = chartData;

                        // pass the above variable to createChart function
                        createChart(
                            title,
                            labels,
                            backgroundColor,
                            chartsData,
                            chartType,
                            displayLegend,
                        );

                        // on click of expand button, render the chart in the charts modal
                        $(document).on("click", "#expand", () => {
                            createChartinModal(
                                title,
                                labels,
                                backgroundColor,
                                chartsData,
                                chartType,
                                displayLegend,
                            );
                        });
                        return;
                    }

                    // check of the custom payload type is "collapsible"
                    if (payload === "collapsible") {
                        const { data } = response[i].custom;
                        // pass the data variable to createCollapsible function
                        createCollapsible(data);
                    }
                }
            }
            scrollToBottomOfResults();
        }
        else {
            // if there is no response from Rasa, send  fallback message to the user
            const fallbackMsg = "দুঃখিত কোনো ধরনের সমস্যা হয়েছে, পুনরায় চেষ্টা করুন";

            // const BotResponse = `<img class="botAvatar" src="./static/img/sara_avatar.png"/><p class="botMsg">${fallbackMsg}</p><div class="clearfix"></div>`;
            const BotResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${fallbackMsg}</p><div class="clearfix"></div>`;
            console.log(response_status)
            $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
            scrollToBottomOfResults();
        }
        $(".usrInput").focus();
    }, 500);

}


function setNIDverificationSuccessful(){
    hideBotTyping();
    const is_verified_message = "NID Verified succesfully";
    const BotResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${is_verified_message}</p><div class="clearfix"></div>`;

    $(BotResponse).appendTo(".chats").hide().fadeIn(2000); 
    scrollToBottomOfResults();
}


function speechNotRecognized(){
    hideBotTyping();
    const is_verified_message = "Speech could not be recognized. Please try again!";

    // const BotResponse = `<img class="botAvatar" src="./static/img/sara_avatar.png"/><p class="botMsg">${fallbackMsg}</p><div class="clearfix"></div>`;
    const BotResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${is_verified_message}</p><div class="clearfix"></div>`;

    $(BotResponse).appendTo(".chats").hide().fadeIn(2000); 
}

function speechRecognize(text){
    if(text == "Speech could not be recognized"){
        speechNotRecognized();
    }
    else {
        $(".usrInput").hide().val(text).fadeIn(500);
	const userInputField = document.querySelector('.usrInput');
	userInputField.focus();
    }
    scrollToBottomOfResults();
}

/**
 * sends the user message to the rasa server,
 * @param {String} message user message
 */
function send(message) {
    $.ajax({
        url: rasa_server_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message, sender: sender_id }),
        success(botResponse, status) {
            console.log("Response from Rasa: ", botResponse, "\nStatus: ", status);
            response_status = status
            console.log("response_status", response_status);

            // if user wants to restart the chat and clear the existing chat contents
            if (message.toLowerCase() === "/restart") {
                $("#userInput").prop("disabled", false);

                // if you want the bot to start the conversation after restart
                // customActionTrigger();
                return;
            }
            TaDaOptionChecker(botResponse[0].text);
            setBotResponse(botResponse);
        },
        error(xhr, textStatus) {
            if (message.toLowerCase() === "/restart") {
                $("#userInput").prop("disabled", false);
            }

            // if there is no response from rasa server, set error bot response
            setBotResponse("");
            console.log("Error from bot end: ", textStatus);
        },
    });
}
/**
 * sends an event to the bot,
 *  so that bot can start the conversation by greeting the user
 *
 * `Note: this method will only work in Rasa 1.x`
 */
// eslint-disable-next-line no-unused-vars


function actionTrigger() {
    $.ajax({
        url: `http://localhost:5005/conversations/${sender_id}/execute`,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            name: action_name,
            policy: "MappingPolicy",
            confidence: "0.98",
        }),
        success(botResponse, status) {
            // console.log("Response from Rasa: ", botResponse, "\nStatus: ", status);

            if (Object.hasOwnProperty.call(botResponse, "messages")) {
                setBotResponse(botResponse.messages);
            }
            $("#userInput").prop("disabled", false);
        },
        error(xhr, textStatus) {
            // if there is no response from rasa server
            setBotResponse("");
            console.log("Error from bot end: ", textStatus);
            $("#userInput").prop("disabled", false);
        },
    });
}

/**
 * sends an event to the custom action server,
 *  so that bot can start the conversation by greeting the user
 *
 * Make sure you run action server using the command
 * `rasa run actions --cors "*"`
 *
 * `Note: this method will only work in Rasa 2.x`
 */
// eslint-disable-next-line no-unused-vars
var response_status= 0;
function customActionTrigger() {
    $.ajax({
        url: "http://localhost:5055/webhook/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            next_action: action_name,
            tracker: {
                sender_id,
            },
        }),
        success(botResponse, status) {
            response_status = status;
            console.log(status);

            // console.log("Response from Rasa: ", botResponse, "\nStatus: ", status);
            if (Object.hasOwnProperty.call(botResponse, "responses")) {
                setBotResponse(botResponse.responses);
            }
            $("#userInput").prop("disabled", false);
        },
        error(xhr, textStatus) {
            // if there is no response from rasa server
            setBotResponse("");
            console.log("Error from bot end: ", textStatus);
            $("#userInput").prop("disabled", false);
        },
    });
}



/**
 * clears the conversation from the chat screen
 * & sends the `/resart` event to the Rasa server
 */
function restartConversation() {
    $("#userInput").prop("disabled", true);
    // destroy the existing chart
    $(".collapsible").remove();

    if (typeof chatChart !== "undefined") {
        chatChart.destroy();
    }

    $(".chart-container").remove();
    if (typeof modalChart !== "undefined") {
        modalChart.destroy();
    }
    $(".chats").html("");
    $(".usrInput").val("");
    send("/restart");
}
// triggers restartConversation function.
$("#restart").click(() => {
    restartConversation();
});

/**
 * if user hits enter or send button
 * */
function displayText(inputText){
    const InitMessage = inputText;
    // const BotResponse = `<img class="botAvatar" src="./static/img/sara_avatar.png"/><p class="botMsg">${InitMessage}</p><div class="clearfix"></div>`;
    const BotResponse = `<img class="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><p class="botMsg">${InitMessage}</p><div class="clearfix"></div>`;
    $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
}
/*
$(document).ready(() => { 

    var userNID = ""; 
    var user_name = "";
    console.log(sender_id);
    var validatedNIDConfirmation = false;
    const InitMessage = "Please first enter your NID: ";
    console.log(`sender id (chat.js):`, sender_id);
    console.log(`ChatbotUserSocketID_socket (inside "chat.js" file):`, ChatbotUserSocketID_socket);
    displayText(InitMessage);
    setTimeout(() => {
        const fetchNID = async () => { 
            try {
                // const response = await fetch('http://127.0.0.1:8080/home/api/user-chatbot/socket/4f0f87410c8145a59a4d9999be8bbc42/'); 
                //const response = await fetch(`http://172.16.6.91/home/api/user-chatbot/socket/${sender_id}/`);
                //const response = await fetch(`http://ibaschat.celloscope.net//home/api/user-chatbot/socket/${sender_id}/`);
                const response = await fetch(`http://${window.location.host}/home/api/user-chatbot/socket/${sender_id}/`);
                const data = await response.json(); 
                userNID = data.user_NID_no; 
                // console.log(`Response Data:`, data);
                user_name = data.first_name + ' ' + data.last_name;
                console.log(`Username:`, user_name);
                // Enable chat input field 
                console.log(`After successfully fetching user NID ('chat.js' file):`, userNID);
                $(".usrInput").removeAttr("disabled"); 
            } catch (error) { 
                console.log(error); 
            } 
        };
        fetchNID()
    }, 1000); 

    // Disable chat input field until NID is validated //

    $(".usrInput").attr("disabled", true); 
    // Function to validate user's NID number 

    const validateNID = (text) => { 
        if (text == userNID) { 
            return true; 
        } else { 
            const InitMessage = "Please enter correct NID: ";
            $("textarea#userInput").val('');
            displayText(InitMessage);
            return false; 
        } 
    }; 
    // Listen for keyup and keypress events on the chat input field 
    $(".usrInput").on("keypress", (e) => { 

        const keyCode = e.keyCode || e.which; 
        var text = $("textarea#userInput").val(); 
        // console.log(text);
        if (keyCode === 13)  /////when pressed enter. This event = 13 
        {
            console.log(text);
            // $(".usrInput").val("");
            if (text === "" || $.trim(text) === "") { 
                e.preventDefault(); 
                return false; 
            } 

            // Validate user's NID number 
            if (validatedNIDConfirmation == false){
                if (!validateNID(text)) {
                    validatedNIDConfirmation = false;
                    return false; 
                }
                else{
                    validatedNIDConfirmation = true;
                    const user_navbar = `<p>User ID: ${userNID} <span id="user-id"></span></p> <p>User Name: ${user_name} <span id="user-name"></span></p>`;
                    $(user_navbar).appendTo(".user-details").hide().fadeIn(1000);
                    $(".chatbox-navbar").toggle();
                    setUserResponse(text); 
		    setNIDverificationSuccessful();
                    e.preventDefault();
                    return false;
                }
            }
             
            else{
                validatedNIDConfirmation = true;
                // Destroy existing chart elements (if any) 
                $(".collapsible").remove(); 
                $(".dropDownMsg").remove(); 
                if (typeof chatChart !== "undefined") { 
                    chatChart.destroy(); 
                } 
                $(".chart-container").remove(); 
                if (typeof modalChart !== "undefined") {
                    modalChart.destroy(); 
                } 
                $("#paginated_cards").remove(); 
                $(".suggestions").remove(); 
                $(".quickReplies").remove(); 
                $(".usrInput").blur(); 
                setUserResponse(text); 
                send(text); 
                e.preventDefault();
                return false; 

            }
        } 
        return true; 
    }); 
}); 
*/
 
///////////////////////////////////////////////

////////////Trial//////////
$(document).ready(() => { 

    var userNID = ""; 
    var user_name = "";
    console.log(sender_id);
    var validatedNIDConfirmation = false;
    const InitMessage = "আপনাকে কিভাবে সাহায্য করতে পারি?";
    console.log(`sender id (chat.js):`, sender_id);
    // console.log(`ChatbotUserSocketID_socket (inside "chat.js" file):`, ChatbotUserSocketID_socket);
    displayText(InitMessage);
    // setTimeout(() => {
    //     const fetchNID = async () => {
    //         try {
    //             //const response = await fetch(`http://127.0.0.1:8080/home/api/user-chatbot/socket/${sender_id}/`);
    //             const response = await fetch(`http://${window.location.host}/home/api/user-chatbot/socket/${sender_id}/`);
                
    //             const data = await response.json(); 
    //             userNID = data.user_NID_no; 
    //             user_name = data.first_name + ' ' + data.last_name;
    //             console.log(`Username:`, user_name);
    //             console.log(`After successfully fetching user NID ('chat.js' file):`, userNID);
    //             $(".usrInput").removeAttr("disabled"); 
    //         } catch (error) { 
    //             console.log(error); 
    //         } 
    //     };
    //     fetchNID()
    // }, 1000); 


    // $(".usrInput").attr("disabled", true); 

    const validateNID = (text) => { 
        if (text == userNID) { 
            return true; 
        } else { 
            const InitMessage = "Please enter correct NID: ";
            $("textarea#userInput").val('');
            // displayText(InitMessage);
            return false; 
        } 
    }; 

    let user_input = document.querySelector("#user-input");

    let userInputEnterHandler = function(e) {
        if (e.key === "Enter") {
          chatbotInputSend(); 
        }
    };

    user_input.addEventListener("keypress", userInputEnterHandler);

    function chatbotInputSend() {
        const input_field_message = user_input.value;
        console.log(`input sent function is called!`);
        console.log("Msg:", input_field_message);
        setUserResponse(input_field_message);
        send(input_field_message);
        // TaDaOptionChecker(inputValue=input_field_message);
        user_input.value = "";
    }
    
    // $(".usrInput").on("keypress", (e) => { 
    //     const keyCode = e.keyCode || e.which; 
    //     var text = $("#userInput").val(); 
	//     var text_trimmed = $("#userInput").val().trim();
    //     console.log(`before clicking enter button value - text:`, text);
    //     console.log(`before clicking enter button value - text_trimmed:`, text_trimmed);
    //     if (keyCode === 13 && text_trimmed!== "") 
    //     {

    //         // if (typeof chatChart !== "undefined") {
    //         //     chatChart.destroy();
    //         // }
        
    //         // $(".chart-container").remove();
    //         // if (typeof modalChart !== "undefined") {
    //         //     modalChart.destroy();
    //         // }
        
    //         $(".suggestions").remove();
    //         $("#paginated_cards").remove();
    //         $(".quickReplies").remove();
    //         $(".usrInput").blur();
    //         $(".dropDownMsg").remove();
    //         // setUserResponse(text);
    //         // send(text);
    //         e.preventDefault();
    //         return false;
    //     } 
    //     return true; 
    // }); 
});

// function removeUserInputEventListener(bot_user_input) {
//     console.log(`Not sending any message to rasa server`);
//     console.log(`Bot user input - after removing the keypress eventListener:`, bot_user_input);
//     bot_user_input.removeEventListener('keypress', userInputEnterHandler);
// }

///////////Trial End//////////////


$("#sendButton").on("click", (e) => {
    const text = $(".usrInput").val();
    if (text === "" || $.trim(text) === "") {
        e.preventDefault();
        return false;
    }
    // destroy the existing chart
    if (typeof chatChart !== "undefined") {
        chatChart.destroy();
    }

    $(".chart-container").remove();
    if (typeof modalChart !== "undefined") {
        modalChart.destroy();
    }

    $(".suggestions").remove();
    $("#paginated_cards").remove();
    $(".quickReplies").remove();
    $(".usrInput").blur();
    $(".dropDownMsg").remove();
    setUserResponse(text);
    send(text);
    e.preventDefault();
    return false;
});
