from gpiozero import MotionSensor , AngularServo , LED
from signal import pause
import gpiod
import os
from time import sleep

# ฟังชั่น LED
def LED_API(LINE,TYPE,SEC=1):
  try:
    led = LED(LINE)
    if SEC == 0 and TYPE == 'on':
      print("SEC เปิดค้าง")
      led.on()
      pause()
    if TYPE == 'on' and SEC > 0:
       print("ON OFF")
       led.on()
       sleep(SEC)
    if TYPE == 'loop' and SEC == 0:
       print("ON SPEED")
       led.blink(0.1,0.1,None,True)
    if TYPE == 'loop' and SEC > 0:
       print("ON LOOP")
       led.blink(SEC,SEC,None,True)

  finally:
    if SEC == 0 :
       return True
    if TYPE == 'loop' :
       return True
    led.off()
    sleep(1)
    print("จบฟังชั้น")

LED_API(22,'on',1)
LED_API(17,'loop',1)
LED_API(22,'on',0)
