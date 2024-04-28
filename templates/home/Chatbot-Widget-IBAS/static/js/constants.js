const action_name = "action_hello_world";
// const rasa_server_url = "http://localhost:5005/";
const rasa_server_url = "http://localhost:5005/webhooks/rest/webhook";
// const rasa_server_url = "https://nlp.celloscope.net/nlp/ibas/chatbot/rest/";
var sender_id = uuidv4();
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const keycloak = Keycloak('./keycloak.json');
