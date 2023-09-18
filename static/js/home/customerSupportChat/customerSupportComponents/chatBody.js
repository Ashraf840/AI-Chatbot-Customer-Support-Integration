// console.log(`Chatbody JS!`);
// console.log(`Chatbody JS! cso_email: ${cso_email}`);
// console.log(`Chatbody JS! reg_user: ${reg_user}`);


// Get the HTML DOM element of chatbox-input-field
// let chatbody_card_footer = document.getElementById("chat-body-card-footer");

// Mutliline Reply Mode (MLR Mode)
let multi_line_reply_container = document.getElementById("mlr-container");
let multi_line_reply = document.getElementById("mlr");
let multi_line_reply_icon = document.getElementById("mlr-icon");
let multi_line_reply_text = document.getElementById("mlr-text");
// console.log(`Chatbox input field:`, chatbody_card_footer);
let mlr_clicked = false;
var multiline_reply_mode = false;   // global variable (exists in both customer & HDO end); toggled inside the "socket.MultilineReplyMode" block of "socket.onmessage" parent block; if the "multiline_reply_mode" is false; only then invoke HF-generate-tocustomer function "human_feedback_query()" from the HDO-end while adding 'chatHTML'.
var sent_msg_by_hdo_in_mlr_mode = false;   // global variable (exists in both customer & HDO end); Whenever the HDO disables the MLR mode w/t even sending any msg to customer, the system won't sent any HF to customer unless the HDO at least sent a single msg, & when the HDO sends a msg while MLR mode is ON, only then this var becomes true in both customer & HDO end, so that while the HDO wants to disable the MLR mode, the system immediately sends an HF to cusotmer end by invoking the "sendHfOnMlrDisable()" func.

// HDO Input Field Query (Query Mode)
let hdo_input_field_query = document.getElementById("hdo-input-field-query");   // This HTML dom initialized/rendered only in the HDO end from the server
let hifq_clicked = false;   // hifq = hdo input field query
let query_mode = false;
let reply_mode = true;

// Conversational Reply Mode (CR Mode)
let conversational_reply_container = document.getElementById("cr-container");
let conversational_reply = document.getElementById("cr");
let conversational_reply_icon = document.getElementById("cr-icon");
let conversational_reply_text = document.getElementById("cr-text");
let cr_clicked = false;
var conversational_reply_mode = false;   // global variable (exists in both customer & HDO end); toggled inside the "socket.ConversationalReplyMode" block of "socket.onmessage" parent block; if the "conversational_reply_mode" is false; only then invoke HF-generate-tocustomer function "human_feedback_query()" from the HDO-end while adding 'chatHTML'.
var sent_msg_by_hdo_in_cr_mode = false;

if (cso_email === "True") {
    // Query/reply modes (HDO)
    hdo_input_field_query.onmouseenter = () => {
        if (!hifq_clicked) {
            // console.log(`Query icon nouse enter!`);
            if (hdo_input_field_query.classList.contains('fa-regular')) {
                // console.log(`Remove "fa-regular" & append "fa-solid"`);
                hdo_input_field_query.classList.remove("fa-regular");
                hdo_input_field_query.classList.add("fa-solid");
                // console.log(`HDO input field icon type:`, hdo_input_field_query);
            }
        }
    };
    hdo_input_field_query.onmouseleave = () => {
        if (!hifq_clicked) {
            // console.log(`Query icon nouse leave!`);
            if (hdo_input_field_query.classList.contains('fa-solid')) {
                // console.log(`Remove "fa-solid" & append "fa-regular"`);
                hdo_input_field_query.classList.remove("fa-solid");
                hdo_input_field_query.classList.add("fa-regular");
            }
        }
    };
    hdo_input_field_query.onclick = () => {
        // console.log(`Query icon is clicked!`);
        hifq_clicked = !hifq_clicked;
        // console.log(`Query icon is clicked:`, hifq_clicked);
        if (hifq_clicked===true) {
            if (hdo_input_field_query.classList.contains('fa-regular')) {
                hdo_input_field_query.classList.remove("fa-regular");
                hdo_input_field_query.classList.add("fa-solid");
            }
        } else {
            if (hdo_input_field_query.classList.contains('fa-solid')) {
                hdo_input_field_query.classList.remove("fa-solid");
                hdo_input_field_query.classList.add("fa-regular");
            }
        }
        hdoQueryReplyMode(hifq=hifq_clicked)
    }

    // Multiline reply mode (HDO)
    multi_line_reply.onmouseenter = () => {
        // Mouse enter will only give visual effects while the "mlr" mode is not enabled
        if (!mlr_clicked) {
            // console.log(`Mouse enter!`);
            multi_line_reply.style.border = "0.1rem solid rgba(52, 71, 103, .5)";
            multi_line_reply.style.boxShadow = "0 0 10px 3px #344767";
            multi_line_reply_icon.setAttribute("fill", "#344767");
            multi_line_reply_text.setAttribute("fill", "white");
            // multi_line_reply_container.classList.add("mlr-container-pop-in");
        }
    };
    
    multi_line_reply.onmouseleave = () => {
        // Mouse leave will only give visual effects while the "mlr" mode is not enabled
        if (!mlr_clicked) {
            // console.log(`Mouse leave!`);
            multi_line_reply.style.border = "0.1rem solid rgb(255, 255, 255, .5)";
            multi_line_reply.style.boxShadow = "0 0 10px 3px #c1c1c1d1";
            multi_line_reply_icon.setAttribute("fill", "white");
            multi_line_reply_text.setAttribute("fill", "#344767");
        }
    };
    
    multi_line_reply.onclick = () => {
        // console.log(`MLR is clicked!`);
        mlr_clicked = !mlr_clicked;     // if "mlr_clicked=true", then make "mlr_clicked=false". Vice versa for the contrary situation
        if (!mlr_clicked) {
            // "mlr_clicked=false" block
            console.log(`mlr onclicked (if):`, mlr_clicked);
            console.log(`HDO has disabled the MLR mode!`);
            multi_line_reply.style.border = "0.1rem solid rgb(255, 255, 255, .5)";
            multi_line_reply.style.boxShadow = "0 0 10px 3px #c1c1c1d1";
            multi_line_reply_icon.setAttribute("fill", "white");
            multi_line_reply_text.setAttribute("fill", "#344767");
            // Make the "sent_msg_by_hdo_in_mlr_mode" to false only if it's made true by the HDO by sending atlest a single msg; this variable will only be true if the HDO sent atleast a single msg.
            // Check if any msg is sent from HDO after enabling the MLR mode, if so, only then invoke the HF sending function immediately after disbaling the MLR mode.
            if (sent_msg_by_hdo_in_mlr_mode===true) {
                sent_msg_by_hdo_in_mlr_mode = false;
                console.log(`sent_msg_by_hdo_in_mlr_mode [multi_line_reply.onclick]:`, sent_msg_by_hdo_in_mlr_mode);
                sendHfOnMlrDisable();
            }
            // invoke a function to send HF (since MLR is switched of) to everyone inside the room through socket

        } else {
            // "mlr_clicked=true" block
            console.log(`mlr onclicked (else):`, mlr_clicked);
            console.log(`HDO has enabled the MLR mode!`);
            multi_line_reply.style.border = "0.1rem solid rgba(52, 71, 103, .5)";
            multi_line_reply.style.boxShadow = "0 0 10px 3px #344767";
            multi_line_reply_icon.setAttribute("fill", "#344767");
            multi_line_reply_text.setAttribute("fill", "white");
        }
        multiLineReplyMode(mlr=mlr_clicked);
    };

    // Conversational Reply Mode (CR)
    conversational_reply.onmouseenter = () => {
        // console.log(`Mouse enter!`);
        if (!cr_clicked) {
            conversational_reply.style.border = "0.1rem solid rgba(52, 71, 103, .5)";
            conversational_reply.style.boxShadow = "0 0 10px 3px #344767";
            conversational_reply_icon.setAttribute("fill", "#344767");
            conversational_reply_text.setAttribute("fill", "white");
        }
    };

    conversational_reply.onmouseleave = () => {
        // console.log(`Mouse leave!`);
        if (!cr_clicked) {
            conversational_reply.style.border = "0.1rem solid rgb(255, 255, 255, .5)";
            conversational_reply.style.boxShadow = "0 0 10px 3px #c1c1c1d1";
            conversational_reply_icon.setAttribute("fill", "white");
            conversational_reply_text.setAttribute("fill", "#344767");
        }
    };

    conversational_reply.onclick = () => {
        console.log(`CR is clicked!`);
        cr_clicked=!cr_clicked;
        if (!cr_clicked) {
            // "cr_clicked=false" block
            console.log(`cr onclicked (if):`, cr_clicked);
            console.log(`HDO has disabled the CR mode!`);
            conversational_reply.style.border = "0.1rem solid rgb(255, 255, 255, .5)";
            conversational_reply.style.boxShadow = "0 0 10px 3px #c1c1c1d1";
            conversational_reply_icon.setAttribute("fill", "white");
            conversational_reply_text.setAttribute("fill", "#344767");
            // Make the "sent_msg_by_hdo_in_cr_mode" to false only if it's made true by the HDO by sending atlest a single msg while MLR mode is on; this variable will only be true if the HDO sent atleast a single msg.
            // Check if any msg is sent from HDO after enabling the CR mode, if so, only then invoke the HF sending function immediately after disbaling the CR mode.
            if (sent_msg_by_hdo_in_cr_mode===true) {
                sent_msg_by_hdo_in_cr_mode = false;
                console.log(`sent_msg_by_hdo_in_cr_mode [conversational_reply.onclick]:`, sent_msg_by_hdo_in_cr_mode);
                sendHfOnCrDisable();
            }
        } else {
            // "cr_clicked=true" block
            console.log(`cr onclicked (else):`, cr_clicked);
            console.log(`HDO has enabled the CR mode!`);
            conversational_reply.style.border = "0.1rem solid rgba(52, 71, 103, .5)";
            conversational_reply.style.boxShadow = "0 0 10px 3px #344767";
            conversational_reply_icon.setAttribute("fill", "#344767");
            conversational_reply_text.setAttribute("fill", "white");
        }
        conversationalReplyMode(cr=cr_clicked);
    }
}