
/**
 * removes the bot typing indicator from the chat screen
 */
function hideBotTyping() {
    $("#botAvatar").remove();
    $(".botTyping").remove();
}

/**
 * adds the bot typing indicator from the chat screen
 */
function showBotTyping() {
    const botTyping = '<img class="botAvatar" id="botAvatar" src="https://st3.depositphotos.com/30456762/37578/v/600/depositphotos_375780486-stock-illustration-chat-bot-robot-avatar-in.jpg"/><div class="botTyping"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div>';
    $(botTyping).appendTo(".chats");
    $(".botTyping").show();
    scrollToBottomOfResults();
}
