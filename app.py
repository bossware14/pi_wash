from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS, cross_origin
import requests
import time
import gpiod
import subprocess
import os
import signal
import json
from datetime import datetime, timezone, timedelta
import socket

#    pip install flask flask-socketio gpiod
#    pip install gunicorn
app = Flask(__name__,template_folder="")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

def StartServer():
    os.system("pkill chromium")
    subprocess.Popen(['chromium-browser','--start-fullscreen','--kiosk', 'http://localhost:5000']) 

def StartApp():
    os.system("pkill chromium")
    subprocess.Popen(['chromium-browser','--start-fullscreen','--kiosk', 'http://localhost:5000/server']) 

# SET ตั้งค่าสายไฟ
# https://youtu.be/W_kdEPdpt8Q
#เปิดและปิด 0.1 วิ
def DELAY_SWIFT(number,value):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1)
  time.sleep(.1)
  led_line.set_value(0)
  led_line.release()
  chip.close()
  return f"success"
 except:
  return f"error"
#เปิด-ปิด 1วินาที
def DELAY_ONE(number,value):
 try:
  LED_PIN = number#17 ขาจ่ายไฟ
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1) #เปิด
  time.sleep(1)
  led_line.set_value(0) #ปิด
  led_line.release()
  chip.close()
  return f"success"
 except:
  led_line.release()
  chip.close()
  return f"error"
#ปิด
def DELAY_STOP(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(0)
  led_line.release()
  chip.close()
  return f"success"
 except:
  return f"error"
#เปิดค้าง
def DELAY_START(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1)
  led_line.release()
  chip.close()
  return f"success"
 except:
  led_line.release()
  chip.close()
  return f"error"

if os.path.isfile('data.json'):
    with open('data.json', 'r') as f:
      json_data = json.load(f)
else:
    json_data = {
  "data": {
    "action": 0,
    "modewash": "modewash1",
    "monitor": "พร้อม",
    "msg": "พร้อม",
    "persen": "0",
    "runtime": "00:00:00",
    "sec": 0,
    "start": 0,
    "status": "STOP",
    "temperature": "temperature1",
    "time": "00:00:00",
    "timeout": "00:00:00",
    "update": "2024-12-01 00:00:00"
  },
  "date": "2024-12-20 00:00:00",
  "id": "a2d08c2d74594940ae6e6d39e96451bb",
  "ip": "127.0.0.1",
  "mode": {
    "modewash1": 15,
    "modewash2": 10,
    "modewash3": 30,
    "modewash4": 25
  },
  "msg": "พร้อมใช้งาน",
  "price": {
    "modewash1": 30,
    "modewash2": 30,
    "modewash3": 50,
    "modewash4": 40,
    "temperature1": 0,
    "temperature2": 30,
    "temperature3": 0
  },
  "status": "ONLINE"
}
    with open('data.json', 'w') as f:
      json.dump(json_data, f) 

#ขาวงจร
pion = {}
pion['led']         = 7 #ไฟแสดง การทำงานของเครื่อง (ไฟโชว)
pion['start']       = 17 #delay เริ่มทำงาน
pion['stop']        = 18 #delay หยุดปั่น
pion['modewash']    = 22 #delay ตั้งค่าการปั่น 1-4
pion['temperature'] = 23 #delay ตั้งค่าอุณภูมิ 1-3
pion['timeout']     = 24 #delay ตั้งค่าเวลา
pion['on']          = 27 #delay อื่นๆ


#ตั้งค่า MODE นาที
jsopn_mode = {}
jsopn_mode['modewash1'] = 15
jsopn_mode['modewash2'] = 10
jsopn_mode['modewash3'] = 30
jsopn_mode['modewash4'] = 25
# Monitor แสดง
mode_wash = {}
mode_wash['modewash1'] = 'ซักปกติ'   #
mode_wash['modewash2'] = 'ซักด่วน'   # 
mode_wash['modewash3'] = 'ผ้าหุ่ม'   #
mode_wash['modewash4'] = 'ถหนอม'   #
mode_wash['temperature1'] = 'อุณหภูมิ ปกติ'   #
mode_wash['temperature2'] = 'อุณหภูมิ น้ำอุ่น'   #
mode_wash['temperature3'] = 'อุณหภูมิ น้ำเย็น'   #
# ตั้งค่า MODE ราคา
jsopn_price = {}
jsopn_price['modewash1'] = 30   #ซักปกติ
jsopn_price['modewash2'] = 25   #ซักด่วน 
jsopn_price['modewash3'] = 50   #ผ้าหุ่ม
jsopn_price['modewash4'] = 40   #ถหนอม
# ความร้อน
jsopn_price['temperature1'] = 0 #ปกติ
jsopn_price['temperature2'] = 30 #น้ำอุ่น
jsopn_price['temperature3'] = 0 #น้ำเย็น

json_data['price'] = jsopn_price
json_data['mode'] = jsopn_mode

@app.route('/')
def index():
    return render_template('index.html')


@socketio.event()
def my_event(message):
    emit('response', {'data': 'got it!'})

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

tz = timezone(timedelta(hours = 7))
json_data['id'] = socket.gethostname()
json_data['date'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
json_data['status'] = 'ONLINE'
json_data['msg'] = 'พร้อมใช้งาน'
json_data['ip'] = get_ip()
json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
print(os.uname())

def update_data(json_data):
    json_data['id'] = socket.gethostname()
    json_data['date'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
    json_data['status'] = 'ONLINE'
    json_data['msg'] = 'พร้อมใช้งาน'
    json_data['ip'] = get_ip()
    json_data['data']['update'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
    json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
    if json_data['data']['start'] ==  1 and json_data['data']['status'] == "START" :
                json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
                t1 = json_data['data']['timeout'].split(':')
                t2 = json_data['data']['time'].split(':')
                HOUR = int(t1[0]) - int(t2[0])
                MIN = int(t1[1]) - int(t2[1])
                SEC = int(t1[2]) - int(t2[2])
                xper = HOUR-MIN-SEC
                if xper <= 0 :
                    json_data['data']['persen'] = 100
                TOSEC = 0
                if HOUR > 0:
                    TOSEC = TOSEC + int(HOUR*60)
                if MIN > 0:
                    TOSEC = TOSEC + int(MIN*60)
                if SEC >= 0:
                    TOSEC = TOSEC + int(SEC)
                else:
                    TOSEC = TOSEC + int(SEC)
                    json_data['data']['runtime'] = str(HOUR)+':'+str(MIN)+':'+str(SEC)
                    json_data['data']['runtime'] = datetime.fromtimestamp(TOSEC).strftime('%M:%S')
                if HOUR <= 0 and MIN <= 0 and SEC <= 0:
                    json_data['data']['TIMSEC'] = 0
                    json_data['data']['runtime'] = "00:00:00"
                    json_data['data']['timeout'] = "00:00:00"
                    json_data['data']['msg'] = "ว่าง"
                    json_data['data']['monitor'] = "เสร็จแล้ว"
                    json_data['msg'] = 'พร้อมใช้งาน'
                    json_data['data']['minute'] = '00:00:00'
                    json_data['data']['status'] = 'STOP'
                    json_data['data']['start'] = 0
                    json_data['data']['action'] = 0
                    json_data['data']['persen'] = 100
                    DELAY_ONE(pion['stop'])
                    DELAY_STOP(pion['led'])
                else:
                    json_data['data']['persen'] = 100-TOSEC*100/int(json_data['data']['sec'])
                    json_data['data']['TIMSEC'] = TOSEC
                    json_data['data']['msg'] = "กำลังทำงาน"
                    json_data['data']['monitor'] = "เครื่องกำลังปั่นผ้า"
                    json_data['data']['start'] = 1
                    json_data['msg'] = 'กำลังซัก'

                with open('data.json', 'w') as f:
                    json.dump(json_data, f) 
                return json_data

    with open('data.json', 'w') as f:
        json.dump(json_data, f) 
    return json_data

@app.route('/api')
def get_api():
    return update_data(json_data),200

@socketio.on('message')
def handleMessage(msg):
    print(msg)
    if msg == 'connect':
        return send(update_data(json_data), broadcast=True)
    else:
       res = json.loads(msg)
       print(res)
       if res["status"] == 'message':
          update_data(json_data)
          return send(json_data, broadcast=True)

       if res["status"] == 'update':
          if json_data['data']['status'] == 'START' and json_data['data']['start'] == 1 :
              json_data['data']['monitor'] = 'เครื่องกำลังทำงาน ไม่สามารถแก้ไขได้'
              return send(json_data, broadcast=True)
          json_data['data'][res["key"]] = res["value"]
          json_data['data']['persen'] = 0
          json_data['data']['update'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
          json_data['data']['monitor'] = 'พร้อมทำงาน'
          if res["key"] == 'modewash':
              DELAY_SWIFT(pion['modewash'],res["value"])
              json_data['data']['monitor'] = mode_wash[res["value"]]
              json_data['data']['action'] = jsopn_mode[res["value"]]
              json_data['data']['price'] = jsopn_price[res["value"]]+jsopn_price[json_data['data']['temperature']]
          if res["key"] == 'temperature':
              DELAY_SWIFT(pion['temperature'],res["value"])
              json_data['data']['monitor'] = mode_wash[res["value"]]
              json_data['data']['action'] = jsopn_mode[json_data['data']['modewash']]
              json_data['data']['price'] = jsopn_price[res["value"]]+jsopn_price[json_data['data']['modewash']]
          
          update = timezone(timedelta(hours=7,minutes=int(json_data['data']['action'])))
          json_data['data']['minute'] = '00:'+str(json_data['data']['action'])+':00'

          DELAY_ONE(pion['timeout'],str(json_data['data']['action']))

          with open('data.json', 'w') as f:
            json.dump(json_data, f) 
          return send(json_data, broadcast=True)

       if res["status"] == 'stop':
          json_data['data']['start'] = 0
          json_data['data']['action'] = 0
          json_data['data']['status'] = 'STOP'
          json_data['data']['TIMSEC'] = 0
          json_data['data']['sec'] = 0
          json_data['data']['persen'] = 0
          json_data['data']['runtime'] = '00:00:00'
          json_data['data']['timeout'] = '00:00:00'
          json_data['data']['monitor'] = 'เสร็จแล้ว'
          json_data['data']['msg'] = 'สิ้นสุดการทำงาน'
          json_data['data']['update'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
          DELAY_ONE(pion['stop'])
          DELAY_STOP(pion['led'])
          with open('data.json', 'w') as f:
            json.dump(json_data, f) 
          return send(json_data, broadcast=True)
          #return send('สิ้นสุดการทำงาน', broadcast=True)

       if res["status"] == 'start':
          mins = int(res["value"])
          update = timezone(timedelta(hours=7,minutes=mins))
          json_data['data']['update'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
          json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
          json_data['data']['timeout'] = datetime.now(tz=update).strftime('%H:%M:%S')
          json_data['data']['action'] = int(mins)
          json_data['data']['sec'] = int(mins)*60
          json_data['data']['runtime'] = '00:00:00'
          json_data['data']['persen'] = '0' 
          json_data['data']['start'] = 1
          json_data['data']['status'] = 'START'
          json_data['data']['monitor'] = 'เริ่มซักผ้า'
          json_data['data']['msg'] = 'เริ่มต้นการทำงาน'
          DELAY_ONE(pion['start'])
          DELAY_START(pion['led'])
          with open('data.json', 'w') as f:
            json.dump(json_data, f) 
          #return send('เริ่มต้นการทำงาน', broadcast=True)
       return send(json_data, broadcast=True)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(f'An error occurred: {e}')

@app.errorhandler(500)
def page_not_s(err):
   return jsonify({"status": "error","code": "500","msg":"ไม่พร้อมใช้งาน"}),200
@app.errorhandler(404)
def page_not_found(err):
   return jsonify({"status": "error","code": "404","msg":"ไม่พร้อมใช้งาน"}),200
@app.errorhandler(400)
def page_not_found_400(err):
   return jsonify({"status": "error","code": "400","msg":"ไม่พร้อมใช้งาน"}),200


###### iot api
# ปิดสวิสทั้งหมด
@app.route('/off',methods=['GET'])
def stop_run():
    LEDSTOP(7)
    LEDSTOP(17)
    LEDSTOP(27)
    LEDSTOP(22)
    LEDSTOP(23)
    LEDSTOP(24)
    LEDSTOP(18)
    msg = {}
    msg['status'] = "success"
    msg['msg'] = "ปิดทั้งหมด"
    return jsonify(msg),200
#เปิดทั่งหมด
@app.route('/on',methods=['GET'])
def on_run():
    LEDSTART(7)
    LEDSTART(17)
    LEDSTART(27)
    LEDSTART(22)
    LEDSTART(23)
    LEDSTART(24)
    LEDSTART(18)
    msg = {}
    msg['status'] = "success"
    msg['msg'] = "เปิดทั้งหมด"
    return jsonify(msg),200
StartServer()
if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",port="5000", debug=True)