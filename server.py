from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import requests
import time
import os
import gpiod
import subprocess
import signal
import json
from datetime import datetime, timezone, timedelta


app = Flask(__name__,template_folder="")
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

 
def StartServer():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:5000']) 
    return True

def StartApp():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:5000']) 
    return True

def ExitApp():
    os.system('python3 app.py')
    os.system('fuser -k 5000/tcp')

def ShutdownApp():
    os.system("fuser -k 5000/tcp")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


#ปิดแอป
@app.route('/close',methods=['GET'])
def KULLSS():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'CLOSE' 
    ExitApp()
    return jsonify(msg),200

@app.route('/shutdown',methods=['GET'])
def Shutdowns():
    os.system("pkill chromium")
    ShutdownApp()
    msg = {}
    msg['msg'] = 'CLOSE' 
    return jsonify(msg),200


@app.route('/stop',methods=['GET'])
def STOPAPP():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'STOP'
    return jsonify(msg),200

#เปิดหน้าใหม่
@app.route('/reload',methods=['GET'])
def RELOAD():
    os.system("pkill chromium")
    StartServer()
    msg = {}
    msg['msg'] = 'RELOAD'
    return jsonify(msg),200

#เปิดหน้าใหม่
@app.route('/start',methods=['GET'])
def START():
    os.system("pkill chromium")
    StartServer()
    msg = {}
    msg['msg'] = 'START'
    return jsonify(msg),200


@app.route('/reboot',methods=['GET'])
def REBOOT():
    os.system('reboot')
    msg = {}
    msg['msg'] = 'REBOOT'
    return jsonify(msg),200

# URL 1
@app.route('/run',methods=['GET'])
def start_run():
    url = request.args.get('on')
    if not url:
        return jsonify({"status": "error"}), 200
    msg = {}
    msg['status'] = SETLED(int(url))
    msg['msg'] = int(url)
    return jsonify(msg),200

@app.route('/')
def index():
    return render_template('server.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True, host='0.0.0.0')
