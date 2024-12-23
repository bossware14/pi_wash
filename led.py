import gpiod
import time
from signal import pause

# ทดสอบ LED  แบบ Loop
def LedLoop(LED_PIN,SEC):
  try:
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    while True:
       print("while Start")
       led_line.set_value(1)  # Turn on the LED
       time.sleep(SEC)  # Wait for 1 second
       led_line.set_value(0)  # Turn off the LED
       print("while End")
       time.sleep(SEC)  # Wait for 1 second
  finally:
   # Release the GPIO line and clean up resources on program exit
       led_line.set_value(0) 
       led_line.release()
       chip.close()
       return print("End And Close")

# เปิด ปิด LED
def LED_START(LED_PIN,VALUE):
  try:
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    while True:
       led_line.set_value(VALUE)  # Turn on the LED
       if VALUE == 1 :
         return print("เปิด")
       else : 
         return print("ปิด")
  finally:
       led_line.release()
       chip.close()



# ทดลอง แบบ loop
LedLoop(17,0.5) 

# แบบ เปิด ปิด
#LED_START(18,1)
