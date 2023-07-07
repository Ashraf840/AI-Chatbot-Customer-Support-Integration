let recorder = null;
// const uploadURL = "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text";
const uploadURL = "http://127.0.0.1:8080/home/api/stt-model/transcribe/";
// const uploadURL = "http://ibaschat.celloscope.net/home/api/stt-model/transcribe/";
const startButton = document.getElementById("recordButton");
// var startButton = document.querySelector("#chat-msg-mic-btn");
const chat_msg_input = document.getElementById("chat-message-input");

startButton.disabled = false;



console.log("Customer support sppech-to-text:", startButton);

if (!navigator.mediaDevices) {
    console.error("getUserMedia not supported.")
}

const constraints = { audio: true };

//the code starts recording the user's voice using navigator.mediaDevices.getUserMedia() function and creates a new MediaRecorder object.

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
            mode: 'no-cors',
            method: "POST",
            cache: "no-cache",
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            console.log("Transcribes response:", result.transcription);
            const text = result.transcription;
            console.log(" -- from server: " + text);
            chat_msg_input.value = text;
        })
        .catch(err => {
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





// function sendTextForDemo(e) {
//     const text = $(".usrInput").val();
//     if (text === "" || $.trim(text) === "") {
//         e.preventDefault();
//         return false;
//     }
//     // destroy the existing chart
//     if (typeof chatChart !== "undefined") {
//         chatChart.destroy();
//     }

//     $(".chart-container").remove();
//     if (typeof modalChart !== "undefined") {
//         modalChart.destroy();
//     }

//     $(".suggestions").remove();
//     $("#paginated_cards").remove();
//     $(".quickReplies").remove();
//     $(".usrInput").blur();
//     $(".dropDownMsg").remove();
//     setUserResponse(text);
//     send(text);
//     e.preventDefault();
//     return false;
// }



$("#recordButton").unbind('click').click( (e) => {

    // if ($(".usrInput").val() !== ""){
    //     sendTextForDemo(e);
    // }

    // else {
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
    // }
    
});













// -----------------------------------------------------------------------------------------------------------------------------------














// let recorder = null;
// const uploadURL = "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text";
// const startButton = document.getElementById("recordButton");
// startButton.disabled = false;

// if (!navigator.mediaDevices) {
//     console.error("getUserMedia not supported.")
// }

// const constraints = { audio: true };

// //the code starts recording the user's voice using navigator.mediaDevices.getUserMedia() function and creates a new MediaRecorder object.

// navigator.mediaDevices.getUserMedia(constraints)
// .then(function(stream) {
//     let chunks = []
//     recorder = new MediaRecorder(stream);


//     recorder.ondataavailable = event => {
//         // Collect all the chunks of the recording in an array.
//         chunks.push(event.data);
//     };



//     recorder.onstop = event => {
//         console.log("Recording stopped.")
//         console.log(`recorder:`, recorder);
//         console.log(`recorder type:`, typeof(recorder));
//         console.log(`recorder mime-type:`, recorder.mimeType);
//         console.log(`Chunks:`, chunks);

//         // Create a blob with all the chunks of the recording.
//         let blob = new Blob(chunks, { type: recorder.mimeType }); 
//         chunks = [];
//         startButton.disabled = false;

//         // Create form data that contain the recording.
//         let formData = new FormData();
//         formData.append("files", blob);
//         console.log(`formData:`, formData);
//         console.log(`audio file:`, blob);
        
//         // headers
//         // const myHeaders = new Headers();
//         // myHeaders.append("Content-Type", recorder.mimeType);
//         // // myHeaders.append("Content-Type", "audio/webm");
//         // myHeaders.append("Access-Control-Allow-Origin", "*");
//         // console.log(`header object:`, myHeaders);

//         // Send the form data to the server.
//         fetch(uploadURL, {
//             method: "POST",
//             // mode: "no-cors",
//             // headers: myHeaders,
//             headers: {
//                 "Access-Control-Allow-Origin":  "http://127.0.0.1:8080",
//                 // "Access-Control-Allow-Methods": "POST",
//                 "Access-Control-Allow-Credentials": "true",
//                 "Content-Type": recorder.mimeType
//                 // "Access-Control-Allow-Headers": ["Content-Type", "Authorization"]
//             },
//             cache: "no-cache",
//             body: formData,
//         })
//         // .then(response => {
//         //     console.log(`Recieved JSON:`, response.json());
//         //     response.json();
//         // }) 
//         .then(response => {
//             console.log(`Received Text:`, response.text());
//             response.text();
//         }) 
//         .then(data => console.log("Received data: ", data))
        
        
//         // .then(resp => {
//         //     if (resp.status === 200) {
//         //         // return resp.json();
//         //         return resp.text();
//         //     } else {
//         //         console.error("Error:", resp)
//         //     }
//         // }).then(resp => {
//         //     const text = resp.text;
//         //     console.log(" -- from server: " + text)

//         //     if (text === "" || $.trim(text) === "") {
//         //         e.preventDefault();
//         //         return false;
//         //     }
//         //     // destroy the existing chart
//         //     if (typeof chatChart !== "undefined") {
//         //         chatChart.destroy();
//         //     }

//         //     $(".chart-container").remove();
//         //     if (typeof modalChart !== "undefined") {
//         //         modalChart.destroy();
//         //     }

//         //     $(".suggestions").remove();
//         //     $("#paginated_cards").remove();
//         //     $(".quickReplies").remove();
//         //     $(".usrInput").blur();
//         //     $(".dropDownMsg").remove();
//         //     setUserResponse(text);
//         //     send(text);
//         //     e.preventDefault();
            
//         //     return false;
            
//         // })
        
//         .catch(err => {
//             console.error(err);
//         });
//     };



//     recorder.onstart = event => {
//         console.log("Recording started.");
//         startButton.disabled = true;
//         // Stop recording when the time is up.
//         // setTimeout(function() { recorder.stop(); }, 5000);
//     };


    
    
// })
// .catch(function(err) {
//     console.error(err);
// });





// function sendTextForDemo() {
//     const text = $(".usrInput").val();
//     if (text === "" || $.trim(text) === "") {
//         e.preventDefault();
//         return false;
//     }
//     // destroy the existing chart
//     if (typeof chatChart !== "undefined") {
//         chatChart.destroy();
//     }

//     $(".chart-container").remove();
//     if (typeof modalChart !== "undefined") {
//         modalChart.destroy();
//     }

//     $(".suggestions").remove();
//     $("#paginated_cards").remove();
//     $(".quickReplies").remove();
//     $(".usrInput").blur();
//     $(".dropDownMsg").remove();
//     setUserResponse(text);
//     send(text);
//     e.preventDefault();
//     return false;
// }



// $("#recordButton").unbind('click').click( (e) => {

//     if ($(".usrInput").val() !== ""){
//         sendTextForDemo();
//     }

//     else {
//         // start recorder
//         if (!startButton.disabled){
//             recorder.start();
//             // startButton.style.backgroundImage = 'linear-gradient(180deg, #ff2038 0%, #ffffff 100%)'
//             document.getElementById('microphone').style = "color:red";
//         }
//         else{
//             recorder.stop();
//             document.getElementById('microphone').style = null;
//         }
//     }
    
// });




