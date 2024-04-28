let recorder = null;
const uploadURL = "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text";
const startButton = document.getElementById("recordButton");
startButton.disabled = false;

if (!navigator.mediaDevices) {
    console.error("getUserMedia not supported.")
}

const constraints = { audio: true };


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

        // Create form data that contain the recording.
        let formData = new FormData();
        formData.append("files", blob);

        // Send the form data to the server.
        fetch(uploadURL, {
            method: "POST",
            cache: "no-cache",
            body: formData
        }).then(resp => {
            if (resp.status === 200) {
                return resp.json();
            } else {
                console.error("Error:", resp)
            }
        }).then(resp => {
            const text = resp.text;
            console.log(" -- from server: " + text)

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
            
        }).catch(err => {
            console.error(err);
        });
    };



    recorder.onstart = event => {
        console.log("Recording started.");
        startButton.disabled = true;
        // Stop recording when the time is up.
        // setTimeout(function() { recorder.stop(); }, 5000);
    };


    
    
})
.catch(function(err) {
    console.error(err);
});





function sendTextForDemo() {
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
}



$("#recordButton").unbind('click').click( (e) => {

    if ($(".usrInput").val() !== ""){
        sendTextForDemo();
    }

    else {
        // start recorder
        if (!startButton.disabled){
            recorder.start();
            // startButton.style.backgroundImage = 'linear-gradient(180deg, #ff2038 0%, #ffffff 100%)'
            document.getElementById('microphone').style = "color:red";
        }
        else{
            recorder.stop();
            document.getElementById('microphone').style = null;
        }
    }
    
});




