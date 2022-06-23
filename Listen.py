
import speech_recognition as sr
import time
from Speak import Say
def Listen():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Đang nghe....")
        r.pause_threshold = 1
        audio = r.listen(source,0,5)

    try:
        print("Đang nhận dạng")
        query = r.recognize_google(audio,language="vi-VN")
        print(f"Bạn Nói: {query}")
    except:
        return ""
    
    query = str(query)
    return query.lower()
def stop():
    Say("Hẹn găp lại sau nha ! ... ")
# def get_text():
#     for i in range(3):
#         text = Listen()
#         if text:
#             return text.lower()
#         elif i < 2:
#             Say("Máy không nghe rõ. Bạn nói lại được không!")
#             time.sleep(3)
#     time.sleep(2)
#     # stop()
#     return 0

def get_text():
    for i in range(3):
        query = Listen()
        if query:
            return query.lower()
        elif i < 2:
            Say("Máy không nghe rõ. Bạn nói lại được không!")
            time.sleep(3)
    time.sleep(2)
    # stop()
    return 0



