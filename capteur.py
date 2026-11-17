import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from db import init_db
from anomalies import init_alertes, enregistrer

# =====================================
# INITIALISATION
# =====================================

init_db()
init_alertes()
GPIO.setmode(GPIO.BCM)

# Capteur DHT11 (temperature + humidite)
dht_sensor = Adafruit_DHT.DHT11
dht_pin = 14

# Capteur de son
sound_pin = 23
GPIO.setup(sound_pin, GPIO.IN)

# Capteur d'eau
water_pin = 18
GPIO.setup(water_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("====================================")
print("   SURVEILLANCE DES CAPTEURS")
print("====================================")

try:
    while True:

        # 1. TEMPERATURE ET HUMIDITE
        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

        if temperature is not None:
            print(f"Temperature = {temperature:.1f} °C")
            enregistrer("capteur1", "temperature", temperature, "°C")
        else:
            print("Temperature = Erreur de lecture")

        if humidity is not None:
            print(f"Humidite = {humidity:.1f} %")
            enregistrer("capteur1", "humidite", humidity, "%")
        else:
            print("Humidite = Erreur de lecture")

        # 2. CAPTEUR D'EAU (1 = eau detectee, 0 = sec)
        water_state = GPIO.input(water_pin)
        print("Eau = Eau detectee" if water_state == GPIO.HIGH else "Eau = Eau non detectee")
        enregistrer("capteur2", "eau", 1 if water_state == GPIO.HIGH else 0, "bool")

        # 3. CAPTEUR DE SON (1 = bruit, 0 = calme)
        sound_state = GPIO.input(sound_pin)
        print("Bruit = Bruit detecte" if sound_state == GPIO.HIGH else "Bruit = Bruit non detecte")
        enregistrer("capteur3", "bruit", 1 if sound_state == GPIO.HIGH else 0, "bool")

        print("------------------------------------")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nArret du programme.")

finally:
    GPIO.cleanup()
    print("GPIO nettoyes.")