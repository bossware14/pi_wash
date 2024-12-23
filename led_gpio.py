from gpiozero import LED
from signal import pause
import gpiod
from time import sleep


def LED_API(LINE,TYPE,SEC=1):
  try:
    led = LED(LINE)

    if SEC == 0 and TYPE == 'on':
      print("SEC 0")
      led.on()
      pause()

    if TYPE == 'on' and SEC > 0:
       print("ON OFF")
       led.on()
       sleep(SEC)

    if TYPE == 'loop' and SEC > 0:
       print("ON LOOP")
       led.blink(SEC,SEC,None,True)
    if TYLE = 'loop' and SEC == 0 :
       print("ON LOOP SLEEP")
       led.blink(0.1,0.1,None,True)
    
  finally:
    if SEC == 0 :
       return True

    if TYPE == 'loop' :
       return True

    led.off()
    sleep(1)
    print("finally")

LED_API(22,'on',1) #เปิด 1 วิ
LED_API(17,'loop',1) #กระพิบ
LED_API(22,'on',0) #เปิดค้าง
