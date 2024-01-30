const inputField = document.querySelector("#userInput");
var tada = {};

inputField.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        let inputFieldValue = inputField.value.toLowerCase();;
        inputField.value = '';
        TaDaOptionChecker(inputValue=inputFieldValue);
    }
});

function TaDaOptionChecker(inputValue) {
    if (inputValue === "ta"
        || inputValue === "da"
        || inputValue === "tada") {
        document.querySelector("#userInput").disabled = true;
        switch (inputValue) {
            case 'ta':
                TavelAllowance('ta');
                break;
            case 'da':
                DailyAllowance('da');
                break;
            case 'tada':
                TavelDailyAllowance('tada');
                break;
            default:
                console.log(`Invalid input type - tada module`);
        }
    }
}
