import secrets
from machine import Pin
from umqtt.simple import MQTTClient
from time import sleep, ticks_ms, ticks_diff

led = Pin(2, Pin.OUT)

contagem = 0
ultimo_valor = -1
ultimo_envio = ticks_ms()

def callback(topic, msg):
    print("Recebido:", topic, msg)

    if topic == secrets.ligaLed:
        if msg == b"1" or msg == b"ON":
            led.on()
            print("LED ON")

        elif msg == b"0" or msg == b"OFF":
            led.off()
            print("LED OFF")

def vib_detectada(pin):
    global contagem
    contagem += 1

mqtt = MQTTClient(
    secrets.AIO_CLIENT,
    secrets.AIO_SERVER,
    port=secrets.AIO_PORT,
    user=secrets.AIO_USERNAME.encode(),
    password=secrets.AIO_KEY.encode()
)

mqtt.set_callback(callback)

print("Conectando MQTT...")
mqtt.connect()
print("MQTT conectado")

mqtt.subscribe(secrets.ligaLed)
print("Inscrito em:", secrets.ligaLed)

mqtt.publish(b"imaicon/feeds/ligaLed/get", b"")

sensor = Pin(13, Pin.IN, Pin.PULL_UP)
sensor.irq(trigger=Pin.IRQ_FALLING, handler=vib_detectada)

while True:

    mqtt.check_msg()

    if ticks_diff(ticks_ms(), ultimo_envio) >= 1000:

        if contagem != ultimo_valor:

            mqtt.publish(
                secrets.aceleracao,
                str(contagem).encode()
            )

            print("Pulsos:", contagem)

            ultimo_valor = contagem

        contagem = 0
        ultimo_envio = ticks_ms()

    sleep(5)
