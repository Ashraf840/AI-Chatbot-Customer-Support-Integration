/**
 *  adds vertically stacked buttons as a bot response
 * @param {Array} suggestions buttons json array
 */

function menuChipsHoverEffectFunc(menuChipId, mouseEnter = false, mouseOut = false) {
    let mcID = `menuChips-${menuChipId}`;
    if (mouseEnter) {
        $(`#${mcID}`).css("background-color", "#872341");
        $(`#${mcID}`).css("font-size", "18px");
        $(`#${mcID}`).css("font-weight", "600");
    }

    if (mouseOut) {
        $(`#${mcID}`).css("background-color", "#060dcfc7");
        $(`#${mcID}`).css("font-size", "14px");
        $(`#${mcID}`).css("font-weight", "400");
    }
}


function addSuggestion(suggestions) {
    console.log("suggestions:", suggestions);
    setTimeout(() => {
        const suggLength = suggestions.length;
        $(
            ' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>',
        )
            .appendTo(".chats")
            .hide()
            .fadeIn(1000);
        // Loop through suggestions
        for (let i = 0; i < suggLength; i += 1) {
            $(
                `<div class="menuChips" id="menuChips-${i}" 
                    onmouseover="menuChipsHoverEffectFunc(menuChipId=${i}, mouseEnter=true, mouseOut=false)" 
                    onmouseout="menuChipsHoverEffectFunc(menuChipId=${i}, mouseEnter=false, mouseOut=true)"
                    data-payload='${suggestions[i].payload}'>${suggestions[i].title}</div>`,
            ).appendTo(".menu");
        }
        scrollToBottomOfResults();
    }, 1000);
}
///////////////////////////////////
function actionsTrigger() {
    $.ajax({
        url: rasa_execute_server,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            name: "action_redirect_website",
            policy: "MappingPolicy",
            confidence: 0.98,
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

function sendEntityValue(message) {
    $.ajax({
        url: rasa_server_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: message, sender: sender_id }),
        success(botResponse, status) {
            response_status = status
            // predicted = 0;
            console.log("response_status", response_status);
            hideBotTyping();
            setBotResponse(botResponse);
        },
        error(xhr, textStatus) {
            if (message.toLowerCase() === "/restart") {
                $("#userInput").prop("disabled", false);
            }

            setBotResponse("");
            console.log("Error from bot end: ", textStatus);
        },
    });
}

///////////////////////////////////

// on click of suggestion's button, get the title value and send it to rasa
//$(document).on("click", ".menu .menuChips", function () {
//    const text = this.innerText;
//    const payload = this.getAttribute("data-payload");
//    console.log("payload: ", this.getAttribute("data-payload"));
//    console.log(`নির্বাচিত বিভাগ হল: ${text}`);
//    messages= `নির্বাচিত বিভাগ হল: ${text}`;
//    sendEntityValue(messages);

// actionsTrigger();
//    setUserResponse(text);
// send(payload);

//    $(".suggestions").remove();
//});

//const csrftoken = getCookie('csrftoken');

function langDetect(text, callback) {
    $.ajax({
        url: lang_detect_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ text: text }),
        headers: {
            'Access-Control-Allow-Origin': '*',
            // "X-CSRFToken": csrftoken,
            // Add any other required headers here
        },
        success(language, status) {
            console.log("bot response: ", language.detected_language);
            console.log("response_status", status);
            //       hideBotTyping();
            const lang = language.detected_language;
            console.log("lang", lang);
            callback(lang);
        },
        error(xhr, textStatus) {
            console.log(xhr, textStatus);
        },
    });
}

$(document).on("click", ".menu .menuChips", function () {
    showBotTyping();
    const text = this.innerText;
    const payload = this.getAttribute("data-payload");
    console.log("payload: ", this.getAttribute("data-payload"));
    console.log(`selected category is ${text}`);
    let message;

    // Call langDetect with a callback function
    // langDetect(text, function (lang) {
    //     console.log("language: ", lang);
    //     if (lang == "bn") {
    //         message = `নির্বাচিত বিভাগ হল: ${text}`
    //     }
    //     else {
    //         message = `selected category is${text}`
    //     }
    // sendEntityValue(message);


    // // Use the detected language here or call actionsTrigger() accordingly
    // });

    send(payload);
    $(".suggestions").remove();
    hideBotTyping()
    setUserResponse(text);
});









