let recorder = null;
let isRecording = false;
// const uploadURL = "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text";
//const uploadURL = "http://127.0.0.1:8080/home/api/stt-model/transcribe/";
const uploadURL = "http://ibaschat.celloscope.net/home/api/stt-model/transcribe/";
// const uploadURL = "http://ibaschat.celloscope.net/home/api/stt-model/transcribe/";
const startButton = document.getElementById("recordButton");
const chat_msg_input = document.getElementById("chat-message-input");

startButton.disabled = false;
const userInput = `<textarea id="userInput" placeholder="Say something..." class="usrInput"></textarea>`
const userInputError = `<textarea id="userInput" placeholder="Something wrong! Please try again..." class="usrInput"></textarea>`
if (!navigator.mediaDevices) {
    console.error("getUserMedia not supported.")
}

const constraints = { audio: true };

function onKeyPressSend(event){

    $(".usrInput").on("keypress", (event) => { 
        const keyCode = event.keyCode || event.which; 
        var text = $("#userInput").val(); 
        if (keyCode == 13) 
        {
            $("#userInput").attr("placeholder", "Say something...");
	    if (text === "" || $.trim(text) === "") {
                event.preventDefault();
                return false;
	    }
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
            event.preventDefault();
            return false;
        } 
        return true; 
    });

}

function addUserInputField(event){
    event.preventDefault();
    $(userInput).appendTo(".keypad");
    onKeyPressSend(event);
}

function appendToUserInputField(text){
    $(".usrInput").val(text).show("slow");
    $(".usrInput").focus();
}


navigator.mediaDevices.getUserMedia(constraints)
.then(function(stream) {
    let chunks = []
    recorder = new MediaRecorder(stream);



    recorder.ondataavailable = event => {
        // Collect all the chunks of the recording in an array.
        chunks.push(event.data);
    };



    recorder.onstop = event => {
        console.log("Recording stopped.")
        // Create a blob with all the chunks of the recording.
        let blob = new Blob(chunks, { type: recorder.mimeType }); 
        chunks = [];
        startButton.disabled = false;

        showLoading();
        // Create form data that contain the recording.
        let formData = new FormData();
        formData.append("files", blob);

        // Send the form data to the server.
        fetch(uploadURL, {
            mode: 'no-cors',
            method: "POST",
            cache: "no-cache",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
        	// Handle 500 Internal Server Error
		if (response.status === 500) {
                hideLoading();
                event.preventDefault();
    $(userInput).appendTo(".keypad");
                $("#userInput").attr("placeholder", "Something wrong! Please try again...");
     		 }}
           
            if (response.transcription == "Speech could not be recognized") {
                console.log("response.ok: ",response.ok)
                $(userInput).appendTo(".keypad");
                $("#userInput").attr("placeholder", "Something wrong! Please try again...");
                hideLoading();
                onKeyPressSend(event);
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(result => {
            console.log("Transcribes response:", result.transcription);
            const text = result.transcription;
            console.log(" -- from server: " + text)
            if (result.transcription == "Speech could not be recognized"){
		hideLoading();
		$(userInputError).appendTo(".keypad");
                //$("#userInput").attr("placeholder", "Something wrong! Please try again...">
                console.log("inside if")
                onKeyPressSend(event);
//                throw new Error("Network response was not ok");
		}
            else{

            if (text === "" || $.trim(text) === "") {
                event.preventDefault();
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
            addUserInputField(event);
            appendToUserInputField(text);
            hideLoading();
            event.preventDefault();
            
            return false;}
        })
        .catch(error => {
	hideLoading();
        event.preventDefault();
        $("#userInput").attr("placeholder", "Something wrong! Please try again...");
        });
    };

    recorder.onstart = event => {
        console.log("Recording started.");
        startButton.disabled = true;
    };   
    
})
.catch(function(err) {
    console.error(err);
});


function sendTextForDemo() {
    const text = $(".usrInput").val();
    if (text === "" || $.trim(text) === "") {
        event.preventDefault();
        return false;
    }
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

    addUserInputField(event);
    appentToUserInputField(text);
    event.preventDefault();
    return false;
}



$("#recordButton").unbind('click').click( (event) => {

    if ($(".usrInput").val() !== ""){
        sendTextForDemo();
    }

    else {
        // start recorder
        if (!startButton.disabled){
            recorder.start();
            document.getElementById('microphone').style = "color:red";
        }
        else{
            recorder.stop();
            document.getElementById('microphone').style = "color:#344767";
        }
    }
    
});

startButton.addEventListener('mousedown', startRecording);
startButton.addEventListener('mouseup', stopRecording);
//document.addEventListener('keydown', handleKeyPress);
//document.addEventListener('keyup', handleKeyRelease);

function startRecording() {
    if (!isRecording && !startButton.disabled) {
        recorder.start();
        document.getElementById('microphone').style = "color:red";
        isRecording = true;
    }
}

function stopRecording() {
    if (isRecording) {
        recorder.stop();
        document.getElementById('microphone').style = null;
        isRecording = false;
    }
}

function handleKeyPress(event) {
    if (event.key === ' ' && !isRecording) {
        startRecording();
    }
}

function handleKeyRelease(event) {
    if (event.key === ' ') {
        stopRecording();
    }
}
