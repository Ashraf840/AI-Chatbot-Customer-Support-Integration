/**
 *  adds vertically stacked buttons as a bot response
 * @param {Array} suggestions buttons json array
 */

// $(document).ready(() => { 
// });
function menuChipsHoverEffectFunc (menuChipId, mouseEnter=false, mouseOut=false) {
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


// on click of suggestion's button, get the title value and send it to rasa
$(document).on("click", ".menu .menuChips", function () {
    const text = this.innerText;
    const payload = this.getAttribute("data-payload");
    console.log("payload: ", this.getAttribute("data-payload"));
    setUserResponse(text);
    send(payload);

    // delete the suggestions once user click on it.
    $(".suggestions").remove();
});
