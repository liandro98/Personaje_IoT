import utime 
import network
import umqtt.simple
from machine import Pin, PWM
from time import sleep
from umqtt.simple import MQTTClient

#Declaro Servo
servo = PWM(Pin(13), freq=50)

# Declaro Buzzer
buzzer = PWM(Pin(12), freq=1, duty=512)

# Posición de grados que tiene el servo
pos = 0

# Iniciamos el servo en la posición inicial
servo.duty(pos)

#WIFI
#definir la propiedad de conexion
MQTT_BROKER= "broker.hivemq.com"
MQTT_CLIENT_ID = ""
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "utng/maeg/camellin"
MQTT_PORT = 1883
#Declaramos una funcion para wifi
def conectar_wifi():
    print("Conectando", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("OPPOA17","z99sksdu")
    while not sta_if.isconnected():
        print(".",end="")
        sleep(0.3)
    print("Wifi conectada!")
    
# Función para tocar la melodía navideña
def tocar_melodia():
    melodia = [
        (659, 500), (659, 500), (784, 500), (659, 500), (987, 500), (880, 1000),
        (784, 500), (698, 500), (659, 500), (987, 500), (880, 1000), (784, 500),
        (698, 500), (659, 500), (1175, 500), (1047, 500), (987, 500), (880, 500),
        (784, 500), (659, 500), (1175, 500), (1047, 500), (987, 500), (880, 500),
        (784, 500), (1175, 500), (1047, 500), (987, 500), (1175, 500), (1319, 500),
        (1047, 500), (987, 500), (784, 500), (1175, 500), (1047, 500), (987, 500),
        (880, 500), (784, 500), (659, 500), (784, 500), (880, 500), (987, 500),
        (1047, 500), (1175, 500), (1319, 500), (1175, 500), (1047, 500), (987, 500),
        (880, 500), (784, 500), (659, 500), (784, 500), (880, 500), (987, 500),
        (1047, 500), (1175, 500), (1319, 500), (1175, 500), (1047, 500), (987, 500),
        (880, 500), (784, 500), (659, 500), (659, 500), (784, 500), (659, 500),
        (1175, 500), (1047, 500), (987, 500), (880, 500), (784, 500), (659, 500),
        (987, 500), (987, 500), (1047, 500), (987, 500), (1175, 500), (1319, 500),
        (1047, 500), (987, 500), (784, 500), (659, 500), (784, 500), (880, 500),
        (987, 500), (1047, 500), (1175, 500), (1319, 500), (1175, 500), (1047, 500),
        (987, 500), (880, 500), (784, 500), (659, 500)
    ]

    melodia_lenta = [
        (659, 500), (659, 500), (659, 500), (523, 500), (659, 500), (784, 500), (392, 500),
        (523, 500), (659, 500), (784, 500), (392, 500), (523, 500), (659, 500), (784, 500),
        (392, 500), (392, 500), (415, 500), (466, 500), (523, 500), (587, 500), (622, 500),
        (659, 500), (698, 500), (784, 500), (880, 500), (784, 500), (698, 500), (659, 500),
        (784, 500), (784, 500), (784, 500), (784, 500), (880, 500), (900, 500), (900, 500),
        (784, 500), (698, 500), (659, 500), (587, 500), (523, 500), (587, 500), (659, 500),
        (698, 500), (784, 500), (880, 500), (784, 500), (698, 500), (659, 500), (784, 500),
        (784, 500), (784, 500), (784, 500), (880, 500), (988, 500), (900, 500), (784, 500),
        (698, 500), (659, 500), (587, 500), (523, 500), (523, 500), (523, 500), (587, 500),
        (659, 500), (698, 500), (784, 500), (880, 500), (784, 500), (698, 500), (659, 500),
        (587, 500), (587, 500), (659, 500), (587, 500), (523, 500)
    ]


    while True:  # Repetir la melodía en un bucle infinito
        for frecuencia, duracion in melodia:
            if 1 <= frecuencia <= 40000000:
                buzzer.freq(frecuencia)
                utime.sleep_ms(duracion)
            else:
                print(f"Frecuencia {frecuencia} está fuera del rango permitido.")
        
        # Pausa entre repeticiones (ajusta según sea necesario)
        utime.sleep_ms(500)
        for frecuencia, duracion in melodia_lenta:
            if 1 <= frecuencia <= 40000000:
                buzzer.freq(frecuencia)
                utime.sleep_ms(duracion)
            else:
                print(f"Frecuencia {frecuencia} está fuera del rango permitido.")
        
        # Pausa entre repeticiones (ajusta según sea necesario)
        utime.sleep_ms(500)

        if recibir_mensaje(client, timeout=2000):  # Espera hasta 5 segundos
                buzzer.freq(1)
                break
        else:
            print("Continua con el bucle")
    
def recibir_mensaje(client, timeout=0):
    start_time = utime.ticks_ms()

    while True:
        if client.check_msg():
            # Se recibió un mensaje
            return True

        current_time = utime.ticks_ms()
        elapsed_time = utime.ticks_diff(current_time, start_time)

        if timeout > 0 and elapsed_time > timeout:
            # Se alcanzó el tiempo máximo de espera
            return False

#Funcion que realiza encender un led y apaga un led 
#De acuerdo al mensaje recibido  del servidor
def llegada_mensaje(topic, msg):
    print("Mensaje: ", msg)
    if msg == b'1':
         while True:
            for pos in range(0, 90):
                servo.duty(pos * 1)
                sleep(0.01)
            # Mover el servo en el rango de 90 a 0 grados
            for pos in range(90, -1, -1):
                servo.duty(pos * 1)
                sleep(0.01)
            if recibir_mensaje(client, timeout=2000):  # Espera hasta 5 segundos
                break
            else:
                print("Continua con el bucle")
    elif msg == b'2':
        print("Tocando melodía navideña")
        tocar_melodia()
        
    else:
        print("Mensaje no valido")

#Funcion que permite la suscripcion al servidor
#Devuelve un cliente
def suscribir():
    client = MQTTClient(MQTT_CLIENT_ID,MQTT_BROKER,port=MQTT_PORT,user=MQTT_USER,
    password=MQTT_PASSWORD,keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectando a: ", MQTT_BROKER,
    "en el topico: ", MQTT_TOPIC)
    return client


#Conectar wifi
conectar_wifi()
#crear objecto wifi
client = suscribir()
while True:
    client.wait_msg()
    sleep(0.5)