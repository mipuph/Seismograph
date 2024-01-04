import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import RPi.GPIO as GPIO
from gpiozero import Button, LED
import time
import threading

token = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
url = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': f'Bearer {token}'}
target_folder = '/var/www/html/media/'  # 目標文件夾路徑

# 上次檢查的圖片列表和影片列表
last_checked_images = set()
last_checked_videos = set()

buzzer_pin = 17
red_led_pin = 25
yellow_led_pin = 8
green_led_pin = 7

GPIO.setwarnings(False)

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(red_led_pin, GPIO.OUT)
    GPIO.setup(yellow_led_pin, GPIO.OUT)
    GPIO.setup(green_led_pin, GPIO.OUT)
   
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(yellow_led_pin, GPIO.LOW)
    GPIO.output(green_led_pin, GPIO.LOW)
    
def activate_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(10)  # 持續20秒
    GPIO.output(buzzer_pin, GPIO.LOW)

def activate_leds():
    end_time = time.time() + 10  # 設置閃燈持續20秒
    while time.time() < end_time:  # 循環閃燈
        GPIO.output(red_led_pin, GPIO.HIGH)
        GPIO.output(yellow_led_pin, GPIO.HIGH)
        GPIO.output(green_led_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(red_led_pin, GPIO.LOW)
        GPIO.output(yellow_led_pin, GPIO.LOW)
        GPIO.output(green_led_pin, GPIO.LOW)
        time.sleep(0.5)

def deactivate_all():
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(yellow_led_pin, GPIO.LOW)
    GPIO.output(green_led_pin, GPIO.LOW)

def send_line_notification(token, message, image_path=None):
    payload = {'message': message}
    if image_path:
        files = {'imageFile': open(image_path, 'rb')}
        response = requests.post(url, headers=headers, data=payload, files=files)
    else:
        response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print('Line notification sent successfully!')
        buzzer_thread = threading.Thread(target=activate_buzzer)
        led_thread = threading.Thread(target=activate_leds)
        
        # 啟動兩個執行緒
        buzzer_thread.start()
        led_thread.start()
        
        # 等待兩個執行緒結束
        buzzer_thread.join()
        led_thread.join()
    else:
        print('Failed to send Line notification...')
        print('Error code:', response.status_code)
     
def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # 附件部分
    attachment = open(attachment_path, 'rb')
    mime_base = MIMEBase('application', 'octet-stream')
    mime_base.set_payload(attachment.read())
    encoders.encode_base64(mime_base)
    mime_base.add_header('Content-Disposition', f'attachment; filename= {attachment_path.split("/")[-1]}')
    message.attach(mime_base)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print('Email sent successfully!')


def check_and_send_email():
    global last_checked_images, last_checked_videos  # 宣告要使用的全局變數
    sender_email = 'your_sender_email'  # Update with your sender email
    sender_password = 'your_sender_password'  # Update with your sender email password
    receiver_email = 'your_receiver_email'  # Update with receiver email
    video_subject = '新增地震影片'
    video_body = 'A new video file has been added to /var/www/html/media/directory.'

    initialize_gpio()  # 初始化 GPIO
   

    while True:
        # 當前圖片列表和影片列表
        current_images = set(filter(lambda x: x.endswith('.jpg'), os.listdir(target_folder)))
        current_videos = set(filter(lambda x: x.endswith('.h264'), os.listdir(target_folder)))
      
        # 檢查是否有新的圖片檔案
        new_images = current_images - last_checked_images
        if new_images:
            for new_image in new_images:
                image_path = os.path.join(target_folder, new_image)
                formatted_time = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y/%m/%d %H:%M:%S')
                line_message = f'有地震快逃阿！我愛大家！時間：{formatted_time}'
                send_line_notification(token, line_message, image_path)
            last_checked_images = current_images

        # 檢查是否有新的影片檔案
        new_videos = current_videos - last_checked_videos
        if new_videos:
            for new_video in new_videos:
                video_path = os.path.join(target_folder, new_video)
                send_email(sender_email, sender_password, receiver_email, video_subject, video_body, video_path)
            last_checked_videos = current_videos
        
        # 每次檢查間隔秒數
        time.sleep(2)  # 可以自行設定檢查的間隔時間

try:
    check_and_send_email()
finally:
    GPIO.cleanup() # 程式終止時關閉 GPIO

