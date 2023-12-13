from machine import Pin
from time import sleep_us
from hcsr04 import HCSR04

# Definir los pines para el sensor de proximidad
trig_pin = Pin(5, Pin.OUT)
echo_pin = Pin(18, Pin.IN)

# Crear una instancia del sensor HC-SR04
sensor_ultrasonido = HCSR04(trig_pin, echo_pin)

# Definir los pines para los LEDs
led1_pin = Pin(12, Pin.OUT)
led2_pin = Pin(4, Pin.OUT)
led3_pin = Pin(22, Pin.OUT)
led4_pin = Pin(15, Pin.OUT)

# Definir la distancia límite para encender los LEDs (en centímetros)
distancia_limite = 15

def medir_distancia():
    distancia = sensor_ultrasonido.distance_cm()
    return distancia

def encender_leds():
    led1_pin.on()
    led2_pin.on()
    led3_pin.on()
    led4_pin.on()

def apagar_leds():
    led1_pin.off()
    led2_pin.off()
    led3_pin.off()
    led4_pin.off()

def main():
    while True:
        distancia = medir_distancia()
        print("Distancia: {} cm".format(distancia))

        if distancia > distancia_limite:
            encender_leds()
        else:
            apagar_leds()

        sleep_us(2000)  # Esperar 1 segundo (1,000,000 us)

main()  # Call the main function directly