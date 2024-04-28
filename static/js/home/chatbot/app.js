// alert("tseting!");
// console.log(csrf_token);

class ChatBox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
        };

        this.state = false; // toggle chatBox collapse
        this.messages = [];
    }

    // Includes event-listeners to chatbox window
    display() {
        const { openButton, chatBox, sendButton } = this.args;
        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({ key }) => {
            if (key == "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    // Toggle chatbox window
    toggleState(chatBox) {
        this.state = !this.state;

        // Show/hide the box
        (this.state) ? chatBox.classList.add('chatbox--active') : chatBox.classList.remove('chatbox--active');
    }

    // Send data to backend func
    onSendButton(chatBox) {
        let inptDom = document.querySelector('input');
        let inpt = inptDom.value;
        // Check if the value is empty
        if (!inpt) {
            // console.log(`Input: empty!`);
            return;
        }
        // console.log(`Input: ${inpt}`);
        const u_msg = { name: "User", message: inpt };
        this.messages.push(u_msg);  // store user msg to messages array
        // this.messages.forEach((element) => console.log(element));

        // Send msg to backend
        const BOT_VIEW = "bot-resp";
        const BOT_URL = `http://${window.location.host}/${BOT_VIEW}/`;
        // console.log(BOT_URL);
        fetch(BOT_URL, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({ 'message': `${inpt}` }) //JavaScript object of data to POST
        })
            .then(response => {
                return response.json(); //Convert response to JSON
            })
            .then(data => {
                //Perform actions with the response data from the view
                const b_msg = { name: "Bot", message: data.answer };
                this.messages.push(b_msg);  // store bot msg to messages array
                // console.log(b_msg['message']);
                // Include chat messages into the chat-display-are
                this.updateChatText(chatBox);
                // Clear value from the chatBox input DOM
                inptDom.value = "";
            })
            .catch((error) => {
                console.log('Error:', error);
                // Include chat messages into the chat-display-are
                this.updateChatText(chatBox);
                // Clear value from the chatBox input DOM
                inptDom.value = "";
            });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach((item) => {
            if (item.name == "Bot") {
                // Invoke the websocket func to craete support request
                if (item.message === "Sure, I'll connect you with an agent") {
                    // Create a support request button; inside that button, the "supportReq()" will be called.
                    html += `<div class="messages__item messages__item--visitor">
                        <button type="button" class="btn btn-info" onclick="supportReq()">Connect</button>
                    </div>`;
                    // supportReq();
                }
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });
        const chatMessage = chatbox.querySelector('.chatbox__messages');
        chatMessage.innerHTML = html;
    }
}


const chatBox = new ChatBox();
chatBox.display();
console.error();