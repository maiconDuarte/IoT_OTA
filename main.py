from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
for _ in range(10):
    led.on()
    sleep(0.25)
    led.off()
    sleep(0.5)
while True:
    pass
