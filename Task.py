import datetime
from time import time
from typing import List
from unittest import result
from Speak import Say
from cgitb import text
from importlib.resources import contents
import os
from tracemalloc import DomainFilter
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
import pyttsx3
from Listen import Listen, get_text
import threading
from tkinter import Label


def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        Say("Chúc bạn buổi sáng tốt lành")
   
    elif hour>=12 and hour<18:  # This uses the 24 hour system so 18 is actually 6 p.m 
        Say("Chúc bạn buổi chiều tốt lành")
 
    else:
        Say("Chúc bạn buổi tối tốt lành")

def play_youtube():
    Say("Nói nội dung bạn muốn tìm trên youtube")
    search = get_text()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    Say("Đây là thứ mà tôi tìm được bạn xem qua nhé")


def play_youtube_2():
    Say("Nói nội dung bạn muốn tìm trên youtube")
    search = get_text()
    while True:
        result = YoutubeSearch(search, max_results=10).to_dict()
        if result:
            break
    url = f"https://www.youtube.com" + result[0]['url_suffix']
    webbrowser.get().open(url)
    Say("Đây là thứ mà tôi tìm được bạn xem qua nhé")
    print(result)

def doihinhnen():
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
    Say("Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không nha ?")

def Time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    Say(time)
def Date():
     now = datetime.datetime.now()
     content = f"hôm nay là ngày {now.day} tháng {now.month} năm {now.year}"
     Say(content)
     return content
def current_weather():
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
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        Say("Không tìm thấy địa chỉ của bạn")
    return content
    
def tell_me_about():
    try:
        Say("Hãy nói cho tôi nghe Bạn muốn tìm gì ạ ?")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        Say(contents[0])
        dem = 0
        for content in contents[1:]:
            if dem < 2:
                Say("Bạn có muốn biết thêm không ???")
                ans = get_text()
                if 'có' not in ans:
                    break
            dem += 1
            Say(content)
        Say("Đây là nội dung tôi vừa tìm được cảm ơn bạn đã lắng nghe")
    except:
        Say(f"{name} không định nghĩa được thuật ngữ của bạn !!!")
def open_app(text):
    if "google" in text:
        Say(f'Mở Google Chrome')
        os.system('"C:\Program Files//Google/Chrome/Application/chrome.exe"')
    elif"microsoft edge" in text:
        Say(f'Mở Microsoft Edge')
        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
    else:
        Say(f'Bạn nói chưa rõ! Hoặc có thể phần mềm chưa cài.')

def help_me():
    Say(f"""
    tôi có thể giúp bạn thực hiện các việc sau đây:
    1. chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng desktop
    4. Tìm kiếm với google
    5. Dự báo thời tiết
    6. Tìm kiếm video với youtube
    7. Thay đổi hình nền máy tính
    8. Tìm kiếm thông tin trên wikipedia
    """)

def NonInputExecution(query):
    query = str(query)
    if "giờ" in query:
        Time()
    elif"ngày" in query:
        Date()
    elif"có thể làm gì" in query:
        help_me()
    elif"lời chào" in query:
        Say("Xin chào. Bạn tên là gì ? ")
        global robot_name
        robot_name = "Duy Tân"
        global name
        name = get_text()
        if name:
            Say(f'Xin chào bạn {name}')
        wishMe()
        Say(f'Bạn cần tôi giúp gì cho bạn đây nè!!!!')
    elif"hình nền" in query:
        doihinhnen()
    elif "định nghĩa" in query:
        tell_me_about()
    elif"thời tiết" in query:
        current_weather()
    elif"mở app" in query:
        open_app()
    elif "youtube" in query:
        Say("Bạn muốn tìm kiếm đơn giản hay phức tạp")
        yeu_cau = get_text()
        if "đơn giản" in yeu_cau:
            play_youtube()
        elif "phức tạp" in yeu_cau:
            play_youtube_2()
            if input("Tiếp tục y/n: ") == "y":
                pass
    else:
        Say(f'Chưa có chức nặng này .Bạn vui lòng yêu cầu chức năng khác nha')
def InputExecution(tag,query):
    if"google" in tag:
        query = str(query).replace("google","")
        query = query.replace("research","")
        import pywhatkit
        pywhatkit.search(query)
    elif "mở chrome" in tag:
        Say(f'Mở Google Chrome')
        os.system('"C:\Program Files//Google/Chrome/Application/chrome.exe"')
    elif"microsoft edge" in tag:
        Say(f'Mở Microsoft Edge')
        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')

