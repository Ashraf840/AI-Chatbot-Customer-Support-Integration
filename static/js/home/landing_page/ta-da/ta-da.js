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
    if (inputValue === "travel_allowance"
        || inputValue === "daily_allowance"
        || inputValue === "travel_and_daily_allowance") {
        document.querySelector("#userInput").disabled = true;
        switch (inputValue) {
            case 'travel_allowance':
                TavelAllowance('ta');
                break;
            case 'daily_allowance':
                DailyAllowance('da');
                break;
            case 'travel_and_daily_allowance':
                TavelDailyAllowance('tada');
                break;
            default:
                console.log(`Invalid input type - tada module`);
        }
    }
}
