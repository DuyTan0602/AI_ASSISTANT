from datetime import date
from Speak import Say
from Listen import get_text
from function import wishMe, current_weather, Date
from Listen import Listen
import datetime
import time
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
from Speak import Say

def action(query):
    if(query =='ngày'):
        now = datetime.datetime.now()
        content = f"hôm nay là ngày {now.day} tháng {now.month} năm {now.year}"
        Say(content)
        return content

    elif(query =='thời tiết'):
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