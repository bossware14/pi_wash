import RPi.GPIO as GPIO
import time

# ตั้งค่า GPIO ให้เป็น output
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# เปิด LED (สมมติว่าต่อ LED ที่ขา GPIO 17)
GPIO.output(17, GPIO.HIGH)
time.sleep(1)

# ปิด LED
GPIO.output(17, GPIO.LOW)

# ทำความสะอาด GPIO
GPIO.cleanup()
