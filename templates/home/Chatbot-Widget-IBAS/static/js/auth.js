function initKeycloak(){
    // keycloak.init({ onLoad: 'login-required', promiseType: 'native' }).success(function (authenticated) {
    //     if (!authenticated) {
    //       console.log('Not authenticated');
    //     } else {
    //       console.log('User authenticated');
    //       sender_id = `${keycloak.subject}_${uuidv4()}`;
    //     }
    //   }).error(function () {
    //     console.log('Authentication failure');
    //   });
    console.log(sender_id);
    console.log(urlParams.get('token'));
}

function logOut(){
    console.log("logging out");
    var logoutOptions = { redirectUri : 'https://nlp.celloscope.net/chatbot/voice/' };
    keycloak.logout(logoutOptions).then((success) => {
            console.log("--> log: logout success ", success );
    }).catch((error) => {
            console.log("--> log: logout error ", error );
    });
}