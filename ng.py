#!/usr/bin/env python
#pip install ngrok
#python3 -m pip install ngrok
#touch ng.py
#NGROK_AUTHTOKEN=2q6m1Gd0w8fEuibiwyToH0JEyfx_2ft99jvARhHn2u8Q2EPe1 python3 ng.py
# import ngrok python sdk
import ngrok
import time

token = '2q6m1Gd0w8fEuibiwyToH0JEyfx_2ft99jvARhHn2u8Q2EPe1'
# Establish connectivity
ngrok.set_auth_token(token)

listener = ngrok.forward(5000, authtoken_from_env=True,authtoken=token)

# Output ngrok url to console
print(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
while True:
    time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")
