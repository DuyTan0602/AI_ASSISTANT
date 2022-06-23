
import random
import json
from unittest import result


import torch

from Brain import NeuralNet
from NeuralNetwork import bag_of_words,tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open("intents.json",encoding='utf-8') as json_data:
    intents = json.loads(json_data.read())

FILE = "huanluyen.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

#------------------------------
Name = "Cris"
from Listen import Listen
from Speak import Say
from Task import NonInputExecution
from Task import InputExecution
def Main():

    sentence = Listen()
    result = str(sentence)
    if sentence =="tạm biệt":
        exit()

# def get_response(msg):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)

    _ , predicted = torch.max(output,dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents ['intents']:
            if tag == intent['tag']:
                reply = random.choice(intent["outputs"])
                if"lời chào" in reply:
                    NonInputExecution(reply)
                elif"giờ" in reply:
                    NonInputExecution(reply)
                elif"ngày" in reply:
                    NonInputExecution(reply)
                elif"thứ" in reply:
                    NonInputExecution(reply)
                elif"có thể làm gì" in reply:
                    NonInputExecution(reply)
                elif"hình nền" in reply:
                    NonInputExecution(reply)
                elif"thời tiết" in reply:
                    NonInputExecution(reply)
                elif"định nghĩa" in reply:
                    NonInputExecution(reply)
                elif"youtube" in reply:
                    NonInputExecution(reply)             
                elif"google" in reply:
                    InputExecution(reply,result)
                elif"mở chrome" in reply:
                    InputExecution(reply,result)
                elif"microsoft adge" in reply:
                    InputExecution(reply,result)
                else:
                    Say(reply)
while True:
    Main()
