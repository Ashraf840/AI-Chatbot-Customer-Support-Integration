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
    if (inputValue === "/utter_calculate_TA"
        || inputValue === "/utter_calculate_DA"
        || inputValue === "/utter_calculate_TADA") {
        document.querySelector("#userInput").disabled = true;
        switch (inputValue) {
            case '/utter_calculate_TA':
                TavelAllowance('ta');
                break;
            case '/utter_calculate_DA':
                DailyAllowance('da');
                break;
            case '/utter_calculate_TADA':
                TavelDailyAllowance('tada');
                break;
            default:
                console.log(`Invalid input type - tada module`);
        }
    }
}



