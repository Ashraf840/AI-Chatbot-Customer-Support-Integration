function hideBotTyping() {
    $("#botAvatar").remove();
    $(".botTyping").remove();
}

function showBotTyping() {
    const botTyping = '<img class="botAvatar" id="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><div class="botTyping"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div>';
    $(botTyping).appendTo(".chats");
    $(".botTyping").show();
    scrollToBottomOfResults();
}


function hideLoadingAnimation() {
    $("#botAvatar").remove();
    $(".loadingAnimation").remove();
}


function showLoadingAnimation() {
    const loadingAnimation = '<div class="loadingAnimation"></div>';
    $(loadingAnimation).appendTo("#form-control")
    $(".loadingAnimation").show();
    
    scrollToBottomOfResults();
}


function hideLoading() {
    console.log("hideLoading")
    $(".loadingAnimation").remove(); // Remove the loading animation
    $(".ms-2").attr("placeholder", "Say something...");
}

function showLoading() {
    console.log("showLoading")
    const loadingAnimation = '<div class="loadingAnimation"><span></span><span></span><span></span></div>';

    // Update the placeholder text in the textarea to "Speech processing..."
    $(".ms-2").attr("placeholder", "Speech processing...");


    $(loadingAnimation).appendTo(".keypad").show("slow");

    $(".usrInput").remove();

}
