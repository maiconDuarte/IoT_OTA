import secrets
from machine import Pin
from umqtt.simple import MQTTClient
from time import sleep, ticks_ms, ticks_diff
from neopixel import NeoPixel

rgb = NeoPixel(Pin(21), 1)

cor_atual = (0, 0, 255)

def led_on():
    rgb[0] = cor_atual
    rgb.write()

def led_off():
    rgb[0] = (0, 0, 0)
    rgb.write()

contagem = 0
ultimo_valor = -1
ultimo_envio = ticks_ms()

def callback(topic, msg):
    global cor_atual
    print("Recebido:", topic, msg)

    if topic == secrets.ligaLed:
        if msg == b"1" or msg == b"ON":
            led_on()
            print("LED ON")

        elif msg == b"0" or msg == b"OFF":
            led_off()
            print("LED OFF")

    if topic == secrets.ledCor:
        if msg in [b"ON", b"OFF", b"1", b"0"]:
            return

        try:
            cor = msg.decode().strip()
            print(repr(cor))

            if cor.startswith('#'):
                cor = cor[1:]

            r = int(cor[0:2], 16)
            g = int(cor[2:4], 16)
            b = int(cor[4:6], 16)

            cor_atual = (r, g, b)
            rgb[0] = cor_atual
            rgb.write()

        except Exception as e:
            print("Erro:", e)

def vib_detectada(pin):
    global contagem
    contagem += 1

mqtt = MQTTClient(secrets.AIO_CLIENT,secrets.AIO_SERVER,port=secrets.AIO_PORT,user=secrets.AIO_USERNAME.encode(),password=secrets.AIO_KEY.encode())

mqtt.set_callback(callback)

def conectar_e_inscrever():
    print("Conectando MQTT...")
    mqtt.connect()
    print("MQTT conectado")
    mqtt.subscribe(secrets.ligaLed)
    mqtt.subscribe(secrets.ledCor)
    print("Inscrito em:", secrets.ligaLed)
    mqtt.publish(secrets.ligaLed + b"/get", b"")
    mqtt.publish(secrets.ledCor + b"/get", b"")

conectar_e_inscrever()

sensor = Pin(13, Pin.IN, Pin.PULL_UP)
sensor.irq(trigger=Pin.IRQ_FALLING, handler=vib_detectada)

while True:
    try:
        mqtt.check_msg()
        if ticks_diff(ticks_ms(), ultimo_envio) >= 1000:
            if contagem != ultimo_valor:
                mqtt.publish(secrets.aceleracao,str(contagem).encode())
                print("Pulsos:", contagem)
                ultimo_valor = contagem
            contagem = 0
            ultimo_envio = ticks_ms()
        sleep(0.05)
    except OSError as e:
        print("Erro:", e)
        sleep(5)
        try:
            conectar_e_inscrever()
        except:
            pass
