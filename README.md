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

<img src="https://github.com/mipuph/Seismograph/blob/main/img/cd.jpg" width = "60%" />

### Step 1 - Enable camera support
Attach camera to RPi
``` sudo raspi-config ```
enabled camera
Update your RPi with the following commands:
``` sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install git
```
Clone the code from github and enable and run the install script with the following commands:
``` git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
```
Then carry on with the installation:
``` ./install.sh```

### Step 2 - LINE notify


```設定line notify可以發送通知
import requests

# 您從 LINE Notify 獲取的權杖（Token）
token ='K6TXNcDVEmPFBjHSyFi1rA6EHtxJy2GfFN3DRFsQehy'
# 要傳送的訊息
message = '有地震救命！我愛大家！'
# LINE Notify 的 API 網址
url = 'https://notify-api.line.me/api/notify'
# 設定 HTTP 請求的標頭
headers = {'Authorization': f'Bearer {token}'}

# 要傳送的資料
payload = {'message': message}
# 發送 POST 請求
response = requests.post(url, headers=headers, data=payload)

# 檢查是否成功發送通知
if response.status_code == 200:
    print('通知已成功發送！')
else:
    print('發送通知失敗...')
    print('錯誤碼:', response.status_code)
```

## Demo Video
https://youtu.be/BuJq_nN8MHI

## Reference
* GPIO：https://pinout.xyz/
*	Web-controlled Raspberry Pi Camera：https://www.youtube.com/watch?v=DutKbZ-Lr8U
*	RPi-Cam-Web-Interface：https://elinux.org/RPi-Cam-Web-Interface
*	LINE notify：https://engineering.linecorp.com/zh-hant/blog/using-line-notify-to-send-stickers-and-upload-images、https://atceiling.blogspot.com/2020/08/raspberry-pi-78bmp180-line-notify.html
*	Email：
*	Buzzer：https://projects.raspberrypi.org/en/projects/physical-computing/9






