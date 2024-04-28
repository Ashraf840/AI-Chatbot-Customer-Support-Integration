
/* module for importing other js files */
function include(file) {
  const script = document.createElement('script');
  script.src = file;
  script.type = 'text/javascript';
  script.defer = true;

  document.getElementsByTagName('head').item(0).appendChild(script);
}


// Bot pop-up intro
document.addEventListener("DOMContentLoaded", () => {
  const elemsTap = document.querySelector(".tap-target");
  // eslint-disable-next-line no-undef
  const instancesTap = M.TapTarget.init(elemsTap, {});
  // instancesTap.open();
  setTimeout(() => {
    // instancesTap.close();
  }, 4000);
});

/* import components */
// include('./static/js/components/index.js');

window.addEventListener('load', () => {

  // initialization
  $(document).ready(() => {
    // let userNID = ""; 
    // var validatedNIDConfirmation = false;
    // console.log(`sender id (scripts.js):`, sender_id);
    // const InitMessage = "Please first enter your NID: ";
    // displayText(InitMessage);
    // const fetchNID = async () => { 
    //     try { 
    //         // const response = await fetch('http://192.168.0.23:8000/home/api/user-chatbot/socket/4f0f87410c8145a59a4d9999be8bbc42/'); 
    //         // const response = await fetch('http://127.0.0.1:8080/home/api/user-chatbot/socket/4f0f87410c8145a59a4d9999be8bbc42/'); 
    //         const response = await fetch(`http://127.0.0.1:8080/home/api/user-chatbot/socket/${sender_id}/`);
    //         const data = await response.json(); 
    //         userNID = data.user_NID_no; 
    //         console.log(`User NID is being fetched successfully "script.js" file!`,userNID);
    //         // Enable chat input field 
    //         $(".usrInput").removeAttr("disabled"); 
    //     } catch (error) { 
    //         console.log(error); 
    //     } 
    // }; 

    // fetchNID();
    
    // Bot pop-up intro
    $("div").removeClass("tap-target-origin");

    // drop down menu for close, restart conversation & clear the chats.
    $(".dropdown-trigger").dropdown();

    // initiate the modal for displaying the charts,
    // if you dont have charts, then you comment the below line
    $(".modal").modal();

    // enable this if u have configured the bot to start the conversation.
    // showBotTyping();
    // $("#userInput").prop('disabled', true);

    // if you want the bot to start the conversation
    // customActionTrigger();
  });
  // Toggle the chatbot screen
  $("#profile_div").click(() => {
    // $(".profile_div").toggle();
    $(".widget").toggle();
  });

  // clear function to clear the chat contents of the widget.
  $("#clear").click(() => {
    $(".chats").fadeOut("normal", () => {
      $(".chats").html("");
      $(".chats").fadeIn();
    });
  });

  // close function to close the widget.
  $("#close").click(() => {
    $(".profile_div").toggle();
    $(".widget").toggle();
    scrollToBottomOfResults();
  });
});





























// /* module for importing other js files */
// function include(file) {
//   const script = document.createElement('script');
//   script.src = file;
//   script.type = 'text/javascript';
//   script.defer = true;

//   document.getElementsByTagName('head').item(0).appendChild(script);
// }



// // Bot pop-up intro (Animation effect)
// document.addEventListener("DOMContentLoaded", () => {
//   const elemsTap = document.querySelector(".tap-target");
//   // eslint-disable-next-line no-undef
//   const instancesTap = M.TapTarget.init(elemsTap, {});
//   instancesTap.open();
//   setTimeout(() => {
//     instancesTap.close();
//   }, 4000);
// });

// /* import components */
// // include('..');
// // import './components/index.js';
// // import {  } from "./components/index.js";

// console.log(`window load er baire!`);

// window.addEventListener('load', () => {
  
//   console.log(`window load`);

//   // var profile_div = document.querySelector('#profile_div');
  
//   // initialization
//   $(document).ready(() => {
//     console.log(`window ready`);

//     let userNID = ""; 
//     var validatedNIDConfirmation = false;
//     const InitMessage = "Please first enter your NID: ";
//     // displayText(InitMessage);
//     const fetchNID = async () => { 
//         try { 
//             // const response = await fetch('http://192.168.0.23:8000/home/api/user-chatbot/socket/4f0f87410c8145a59a4d9999be8bbc42/'); 
//             const response = await fetch('http://127.0.0.1:8080/home/api/user-chatbot/socket/4f0f87410c8145a59a4d9999be8bbc42/'); 
//             const data = await response.json(); 
//             userNID = data.user_NID_no; 
//             console.log(userNID);
//             // Enable chat input field 
//             $(".usrInput").removeAttr("disabled"); 
//         } catch (error) { 
//             console.log(error); 
//         } 
//     }; 

//     fetchNID(); 

//     // Bot pop-up intro
//     $("div").removeClass("tap-target-origin");

//     // drop down menu for close, restart conversation & clear the chats.
//     $(".dropdown-trigger").dropdown();

//     // initiate the modal for displaying the charts,
//     // if you dont have charts, then you comment the below line
//     $(".modal").modal();

//     // enable this if u have configured the bot to start the conversation.
//     // showBotTyping();
//     // $("#userInput").prop('disabled', true);

//     // if you want the bot to start the conversation
//     // customActionTrigger();
//   });




//   // // Toggle the chatbot screen
//   // profile_div.addEventListener("click", () => {
//   //   console.log(`testing profile-div click event!`);
//   // })

//   $("#profile_div").click(function() {
//     console.log(`testing again! chat.js-1`);

//     $(".profile_div").toggle();
//     console.log(`testing again! chat.js-2`);

//     $(".widget").toggle();
//     console.log(`testing again! chat.js-3`);

//   });

//   // clear function to clear the chat contents of the widget.
//   $("#clear").click(() => {
//     $(".chats").fadeOut("normal", () => {
//       $(".chats").html("");
//       $(".chats").fadeIn();
//     });
//   });

//   // close function to close the widget.
//   $("#close").click(() => {
//     $(".profile_div").toggle();
//     $(".widget").toggle();
//     scrollToBottomOfResults();
//   });







// //   function include(file) {
// //     const script = document.createElement('script');
// //     script.src = file;
// //     script.type = 'text/javascript';
// //     script.defer = true;

// //     document.getElementsByTagName('head').item(0).appendChild(script);
// // }









// });
