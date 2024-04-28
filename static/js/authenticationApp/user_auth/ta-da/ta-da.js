// const inputField_gen = document.querySelector("#user-input");
var tada = {};
// inputField_gen.addEventListener("keypress", function(event) {
//     if (event.key === "Enter") {
//         event.preventDefault();
//         let inputField_genValue = inputField_gen.value.toLowerCase();;
//         inputField_gen.value = '';
//         TaDaOptionChecker(inputValue=inputField_genValue);
//     }
// });

function TaDaOptionChecker(inputValue) {
    console.log(`tada module called in login page!`);
    console.log("inputValue:", inputValue);
    // console.log("inputField_gen:", inputField_gen);
    if (inputValue === "travel_allowance"
        || inputValue === "daily_allowance"
        || inputValue === "travel_and_daily_allowance") {
        document.querySelector("#user-input").disabled = true;
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
