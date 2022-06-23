import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader

from NeuralNetwork import bag_of_words, lower, tokenize,stem
from Brain import NeuralNet

with open('intents.json', 'r',encoding='utf-8') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    for pattern in intent['patterns']:
        # print(pattern)
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

ignore_words = [',','?','/','.','!'] #loai bo cac dau 

all_words = [lower(w) for w in all_words if w not in ignore_words] 
# Sắp xếp và lưu vào hai tệp pattern và tags
all_words = sorted(set(all_words)) 
tags = sorted(set(tags))

#gán biến dữ liệu dùng để huấn luyện
X_train = []
y_train = []


for (pattern_sentence,tag) in xy:
    bag = bag_of_words(pattern_sentence,all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)
#chuyen sang dang array: vector
X_train = np.array(X_train)
y_train = np.array(y_train)

num_epochs = 1000
batch_size =8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)

print("Đang huấn luyện...")

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]

    def __len__(self):
        return self.n_samples

dataset = ChatDataset()

train_loader = DataLoader(dataset=dataset,
                          batch_size = batch_size,
                          shuffle = True,
                          num_workers=0)

device = torch.device('cuda'if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size,hidden_size,output_size).to(device=device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

# #Train The Model
for epoch in range(num_epochs):
    for(words,labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        outputs = model(words)

        loss = criterion(outputs ,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if(epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}],Loss:{loss.item():.4f}')

print(f'Sai Số : {loss.item():.4f}')

data = {
    "model_state":model.state_dict(),
    "input_size":input_size,
    "hidden_size":hidden_size,
    "output_size":output_size,
    "all_words":all_words,
    "tags":tags
}

FILE = "TrainData.pth"
torch.save(data,FILE)

print(f"Training Complete,File Saved To {FILE}")