function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         // console.log(cookies);
//         console.log("getCookie(name):", name);
//         console.log("getCookie(name) length:", name.length);
//         for (var i = 0; i < cookies.length; i++) {
//             // var cookie = jQuery.trim(cookies[i]);
//             var cookie = cookies.pop();
//             console.log(cookie);
//             console.log(cookie.substring(0, name.length + 1) === (name + '='));
//             console.log(decodeURIComponent(cookie.substring(name.length + 1)));
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;}