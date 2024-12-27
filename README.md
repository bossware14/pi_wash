# Raspberry Pi5 Websocket Api
แอปเชื่อมต่อ PION ของ Raspberry Pi5

# Auto Start
sudo crontab -e

1

@reboot python3 ~/Desktop/pi_wash/app.py &

# โหลดโปรเจค Git Clone
cd ~/Desktop

git clone https://github.com/bossware14/pi_wash.git

cd pi_wash

pip install flask flask-socketio gpiod flask-cors

python3 app.py
# เชคการอัพเดทล่าสุด

cd ~/Desktop/pi_wash

git pull https://github.com/bossware14/pi_wash.git
 
# โปรดติดตั้ง Python 3
pip install flask flask-socketio gpiod flask-cors

# วิธีรัน
python3 app.py

# Server
port 5000

# บทความ
พอร์ตอินพุตเอาต์พุตอเนกประสงค์ หรือ GPIO ของ RaspberryPi 3 - INEX

https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://inex.co.th/store/manual/Rpi302-019046-opt.pdf&ved=2ahUKEwiks4_X17mKAxUHXWwGHbReGZkQFnoECDIQAQ&usg=AOvVaw2D6IqF5-QmBu2FOsj0QPSb

https://raspberrypi3robot.blogspot.com/2018/07/?m=1
