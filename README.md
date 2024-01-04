# IOT Project - Mipu’s Seismograph
<img src="https://github.com/mipuph/Seismograph/blob/main/img/kitty.jpg" width = "20%" /><img src="https://github.com/mipuph/Seismograph/blob/main/img/kitty.jpg" width = "20%" /><img src="https://github.com/mipuph/Seismograph/blob/main/img/kitty.jpg" width = "20%" />
## About Project
This project is about an online earthquake alert system using a Raspberry Pi 4. The Raspberry Pi device is placed securely inside a building. When the building experiences shaking, the camera detects motion in the camera footage. It captures photos along with the time of the earthquake and sends this information to the user's LINE notify. Additionally, it emails a video of the shaking process to a designated email address. When motion is detected, a buzzer will sound, and LED lights will flash as a visual reminder.

## Hardware Components
1.	Raspberry Pi Model B*1
2.	Pi Camera*1
3.	Breadboard*1
4.	Steel ball*1 (at least)
5.	Buzzer(HPE-122)*1
6.	220 ohm resistor*3
7.	DC12V LED*3
8.	Wire, tape
9.	Thick cardboard
10.	Dupont Lines Pi*6 (at least)

<img src="https://github.com/mipuph/Seismograph/blob/main/img/mipu.jpg" width = "50%" />

## Circuit Diagram

<img src="https://github.com/mipuph/Seismograph/blob/main/img/cd.jpg" width = "70%" />

### Step 1 - Enable camera support
Attach camera to RPi and enable camera support 
```
sudo raspi-config 
```

enabled camera

Update your RPi with the following commands：
```
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install git
```
Clone the code from github and enable and run the install script with the following commands：
```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
```
Then carry on with the installation:
``` 
./install.sh
```
<img src="https://github.com/mipuph/Seismograph/blob/main/img/pic1.jpg" width = "50%" />

Then start camera interface. Open web browser and enter camera ip and cam subfolder：

e.g. http://raspberrypi_ip/html/index.php

<img src="https://github.com/mipuph/Seismograph/blob/main/img/pic2.jpg" width = "50%" /><img src="https://github.com/mipuph/Seismograph/blob/main/img/pic3.jpg" width = "50%" />

All camera function settings can be modified in the web interface

### Step 2 - LINE notify and send_email

<img src="https://github.com/mipuph/Seismograph/blob/main/img/line6.jpg" width = "60%" />

Log in to line notify official website(https://notify-bot.line.me/en/),
* Click `My page` and `Generate token`

<img src="https://github.com/mipuph/Seismograph/blob/main/img/line1.jpg" width = "30%" />   <img src="https://github.com/mipuph/Seismograph/blob/main/img/line2.jpg" width = "30%" />

* Generate personal account Token
  
    1.Enter a Token name and `select 1-to-1 chat with LINE Notify`
  
    2.Click `Generate token` button
  
    3.Click `Copy` button


<img src="https://github.com/mipuph/Seismograph/blob/main/img/line4.jpg" width = "30%" />   <img src="https://github.com/mipuph/Seismograph/blob/main/img/line3.jpg" width = "30%" />

* Use the token test line notify to send notifications

```
import requests

#您從LINE Notify獲取的權杖（Token）
oken ='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
#要傳送的訊息
message = '有地震救命！我愛大家！'
#LINE Notify的API網址
url = 'https://notify-api.line.me/api/notify'
#設定HTTP請求的標頭
headers = {'Authorization': f'Bearer {token}'}

#要傳送的資料
payload = {'message': message}
#發送POST請求
response = requests.post(url, headers=headers, data=payload)

#檢查是否成功發送通知
if response.status_code == 200:
    print('通知已成功發送！')
else:
    print('發送通知失敗...')
    print('錯誤碼:', response.status_code)
```

 * Test sending an email and attaching a video file

```
def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

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
```

### Step 3 - Add a Buzzer and LED lights




## Demo Video
https://youtu.be/BuJq_nN8MHI

## Reference
* GPIO：https://pinout.xyz/
*	Web-controlled Raspberry Pi Camera：https://www.youtube.com/watch?v=DutKbZ-Lr8U
*	RPi-Cam-Web-Interface：https://elinux.org/RPi-Cam-Web-Interface
*	LINE notify：https://engineering.linecorp.com/zh-hant/blog/using-line-notify-to-send-stickers-and-upload-images、https://atceiling.blogspot.com/2020/08/raspberry-pi-78bmp180-line-notify.html、https://notify-bot.line.me/en/
*	Email：https://forums.raspberrypi.com/viewtopic.php?t=325558
*	Buzzer：https://projects.raspberrypi.org/en/projects/physical-computing/9






