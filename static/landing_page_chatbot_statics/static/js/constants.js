const action_name = "action_hello_world";
// const rasa_server_url = "http://localhost:5005/";
const rasa_server_url = "http://127.0.0.1:5005/webhooks/rest/webhook";
//const rasa_server_url = "http://172.16.6.91:5005/webhooks/rest/webhook";
//const rasa_server_url = "http://ibaschat.celloscope.net/webhooks/rest/webhook";
// const rasa_server_url = "http://ibaschat.celloscope.net/rasa/webhooks/rest/webhook";
// const rasa_execute_server = "http://ibaschat.celloscope.net/conversations/${sender_id}/execute";
// const rasa_server_url = "https://nlp.celloscope.net/nlp/ibas/chatbot/rest/";
// const lang_detect_url = "http://ibaschat.celloscope.net/home/api/language-detection/detect"
const lang_detect_url = "http://127.0.0.1:8080/home/api/language-detection/detect"
//const lang_detect_url - "http://172.16.6.91:80/home/api/language-detection/detect"
var sender_id = uuidv4();
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const keycloak = Keycloak('./keycloak.json');
