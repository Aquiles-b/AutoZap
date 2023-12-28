import time
import webbrowser as web
from datetime import datetime
from urllib.parse import quote
import pyautogui as pg

WAIT_TIME = 14

def waitUntil(time_hour, time_min):
    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )
    sleep_time = left_time.seconds - WAIT_TIME
    print(sleep_time)
    time.sleep(sleep_time)

def send_message(phone_no, message):
    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    screenWidth, screenHeight = pg.size()
    time.sleep(WAIT_TIME)
    pg.press('f11')
    time.sleep(1)
    pg.click(screenWidth/2, screenHeight*0.94)
    pg.press('enter')
    pg.press('f11')
    time.sleep(4)
    pg.hotkey('ctrl', 'w')

phone = input("Enter phone number (DDD912345678): ")
message = input("Enter message: ")
hour = input("Enter hour(24h): ")
if hour != '':
    hour = int(hour)
    minute = input("Enter minute: ")
    if minute == '':
        minute = 0
    else:
        minute = int(minute)
    waitUntil(hour, minute)

send_message(phone, message)
