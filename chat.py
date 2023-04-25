import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from staffApp.cso_connectivity_models import CSOOnline
from home.models import CustomerSupportRequest

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open("intents.json", "r") as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# Create the bot
bot_name = "Bot"
# print("Let's chat! Type 'quit/bye' to exit.")


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                if intent['tag'] == "customersupport":
                    active_cso = CSOOnline.get_active_cso()
                    print(f'total active cso: {len(active_cso)}')
                    if len(active_cso) == 0:
                        return "No CSO is currently available! A CSO will contact with you soon!"
                    if len(active_cso) == 1:
                        print(f'Active cso: {active_cso[0]["cso_email"]}')
                        total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso(cso_email=active_cso[0]["cso_email"])
                        # print(f'Total msg of the CSO {active_cso[0]["cso_email"]: {total_msg}}')
                        print(f'Total msg: {len(total_msg)}')
                        if len(total_msg) >= 5:
                            return "No CSO is currently available! A CSO will contact with you soon!"
                        else:
                            print(f'The chat will be routed to {active_cso[0]["cso_email"]}')
                    if len(active_cso) > 1:
                        total_msg = CustomerSupportRequest.get_reqs_with_assigned_cso()
                        msg_req = []
                        for msg in total_msg:
                            msg_req.append(msg['assigned_cso'])
                        msg_req_set = set(msg_req)
                        msg_count = []
                        msg_req_list = list(msg_req_set)
                        for i in msg_req_list:
                            msg_count.append(msg_req.count(i))
                        for x in msg_count:
                            if x < 5:   # if there is any cso whose handling less than 5 chats at the current moment
                                return random.choice(intent['responses'])
                        return "No CSO is currently available! A CSO will contact with you soon!"
                return random.choice(intent['responses'])
    return "I do not understand..."



if __name__ == "__main__":
    print("Let's chat! (type 'quit/bye' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit" or sentence == "bye":
            print(f"Bye! Have a nice day.")
            break

        resp = get_response(sentence)
        print(resp)


# while True:
#     sentence = input('You: ')
#     if sentence == "quit" or sentence == "bye":
#         print(f"{bot_name}: Bye! Have a nice day.")
#         break
