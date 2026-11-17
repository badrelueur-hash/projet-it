import time
import Adafruit_DHT

# Capteur DHT11 sur le GPIO 14
sensor = Adafruit_DHT.DHT11
pin = 14

print("Test du DHT11 (Ctrl+C pour arrêter)")

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if temperature is not None:
            print(f"Température = {temperature:.1f} °C | Humidité = {humidity:.1f} %")
        else:
            print("Échec de lecture du capteur.")

        time.sleep(2)  
        

except KeyboardInterrupt:
    print("\nArrêt du test.")