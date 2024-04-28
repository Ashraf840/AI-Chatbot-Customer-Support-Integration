import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
import torch
import torch.nn as nn

with open('intents.json') as f:
    intents = json.load(f)

# print(intents)
all_words = []
tags = []
xy = []     # contains all the tokenized words & their corresponding patterns

# loop over the "intents" key-value pair which primarily contains "a list"
for intent in intents['intents']:
    tag = intent['tag']     # each intent elem contains a dict
    tags.append(tag)    # each "tag" key's value is appended into "tags" list
    # loop over the "input" key-value pair of each intent elem
    for inpt in intent['input']:
        # toeknized every inputs (sentences in words)
        w = tokenize(inpt)
        all_words.extend(w) # adds all the elements of an iterable (list, tuple, string etc.) to the end of the list.
        xy.append((w, tag))

ignore_words = ["?", "!", ".", ","]
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
# print(all_words)
# print(tags)

# Create trainig dataset list
X_train = []
y_train = []


for (pattern_sent, tag) in xy:
    bag = bag_of_words(pattern_sent, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)   # store only the index-value of labels

# Convert into numpy array
X_train = np.array(X_train)
y_train = np.array(y_train)
# print(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples

# Hyper-parameter
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 1000
# print(input_size, len(all_words))
# print(output_size, tags)

# Initialize chatDataset
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss & optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# training loop
for epoch in range(num_epochs):
    # training loader
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)
        # forward pass
        outputs = model(words)
        loss = criterion(outputs, labels.long())
        # backward & optimizer step
        optimizer.zero_grad() # empty the gradients
        loss.backward()
        optimizer.step() # calculate back propagation
    
    if (epoch+1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}; loss={loss.item():.4f}')

print(f'final loss;  loss={loss.item():.4f}')


# Save/load model
# Save the data
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)  # serialize & save as pickled file

print(f"Training complete. File saved to {FILE}")