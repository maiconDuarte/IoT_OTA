from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)  # GPIO 2 é o LED interno na maioria dos ESP32

while True:
    led.on()
    sleep(0.25)
    led.off()
    sleep(0.5)
