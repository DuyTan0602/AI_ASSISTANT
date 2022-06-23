import queue
import random
import json
import torch
import datetime
from Brain import NeuralNet
from NeuralNetwork import bag_of_words,tokenize
from trolyao import action
from Listen import get_text
import requests
import webbrowser
import urllib.request as urllib2
import os
import ctypes
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

def get_response(msg):
    sentence = tokenize(msg)
    if(msg =="không xác định"):
        return " Chức năng này tạm thời chưa có"
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
                #  print( intent["tag"])
                #  return action(tag)
                reply =  random.choice(intent["outputs"])
                if"giờ" in reply:
                    time = datetime.datetime.now().strftime("%H:%M:%S")
                    Say(time)
                    return time
                elif"ngày" in reply:
                    now = datetime.datetime.now()
                    content = f"hôm nay là ngày {now.day} tháng {now.month} năm {now.year}"
                    Say(content)
                    return content
                    
                elif"thời tiết" in reply:
                    Say("Bạn muốn xem thời tiết ở đâu ạ.")
                    # Đường dẫn trang web để lấy dữ liệu về thời tiết
                    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
                    # lưu tên thành phố vào biến city
                    city = get_text()
                    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
                    if not city:
                        pass
                    # api_key lấy trên open weather map
                    api_key = "b4750c6250a078a943b3bf920bb138a0"
                    # tìm kiếm thông tin thời thời tiết của thành phố
                    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
                    # truy cập đường dẫn của dòng 188 lấy dữ liệu thời tiết
                    response = requests.get(call_url)
                    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
                    data = response.json()
                    # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
                    if data["cod"] != "404":
                        # lấy value của key main
                        city_res = data["main"]
                        # nhiệt độ hiện tại
                        current_temperature = city_res["temp"]
                        # áp suất hiện tại
                        current_pressure = city_res["pressure"]
                        # độ ẩm hiện tại
                        current_humidity = city_res["humidity"]
                        # thời gian mặt trời
                        suntime = data["sys"]
                        # 	lúc mặt trời mọc, mặt trời mọc
                        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
                        # lúc mặt trời lặn
                        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
                        # thông tin thêm
                        wthr = data["weather"]
                        # mô tả thời tiết
                        weather_description = wthr[0]["description"]
                        # Lấy thời gian hệ thống cho vào biến now
                        now = datetime.datetime.now()
                        # hiển thị thông tin với người dùng
                        content = f"""
                        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
                        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
                        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
                        Nhiệt độ trung bình là {current_temperature} độ C
                        Áp suất không khí là {current_pressure} héc tơ Pascal
                        Độ ẩm là {current_humidity}%
                        """
                        Say(content)
                    else:
                        Say("Không tìm thấy địa chỉ của bạn")
                    return content
                elif "lời chào" in reply:
                    hour=datetime.datetime.now().hour
                    if hour>=0 and hour<12:
                        content = "Chúc bạn buổi sáng tốt lành"
                        Say("Chúc bạn buổi sáng tốt lành")
                        return content
                
                    elif hour>=12 and hour<18: 
                        content =  "Chúc bạn buổi chiều tốt lành" 
                        Say("Chúc bạn buổi chiều tốt lành")
                        return content
                
                    else:
                        content =  "Chúc bạn buổi tốt tốt lành" 
                        Say("Chúc bạn buổi tối tốt lành")
                        return content

                elif"có thể làm gì" in reply:
                    content = f"""
                        tôi có thể giúp bạn thực hiện các việc sau đây:
                        1. chào hỏi
                        2. Hiển thị giờ
                        3. Mở website, ứng dụng desktop
                        4. Tìm kiếm với google
                        5. Dự báo thời tiết
                        6. Tìm kiếm video với youtube
                        7. Thay đổi hình nền máy tính
                        8. Tìm kiếm thông tin trên wikipedia
                        """
                    Say(content)
                    return content
                elif"youtube" in reply:
                    Say("Nói nội dung bạn muốn tìm trên youtube")
                    search = get_text()
                    url = f"https://www.youtube.com/search?q={search}"
                    webbrowser.get().open(url)
                    content ="Đây là thứ mà tôi tìm được bạn xem qua nhé"
                    Say(content)
                    return content
                elif "hinh nền" in reply:
                    api_key = "XFyV6boeltUQBb9ROo5nPsWWvoPPDCPLRSwMaO_IXc4"
                    url = 'https://api.unsplash.com/photos/random?client_id=' + \
                        api_key  # pic from unspalsh.com
                    f = urllib2.urlopen(url)
                    json_string = f.read()
                    f.close()
                    parsed_json = json.loads(json_string)
                    photo = parsed_json['urls']['full']
                    # Location where we download the image to.
                    urllib2.urlretrieve(photo, "C:\\Users\\ADMIN\\OneDrive\\Desktop\\AI\\PROJECT_CK\\a.png")
                    image = os.path.join("C:\\Users\\ADMIN\\OneDrive\\Desktop\\AI\\PROJECT_CK\\a.png")
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
                    content ="Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không nha ?"
                    Say(content)
                    return content
                
                elif "mở app " in reply:
                    if"google" in reply:
                        content = f'Mở Google Chrome'
                        Say(content)
                        os.system('"C:\Program Files//Google/Chrome/Application/chrome.exe"')
                        return content
                    elif"microsoft edge" in reply:
                        content = f'Mở Microsoft Edge'
                        Say(content)
                        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
                        return content
                else:    
                    return" tôi không hiểu"
    
            


