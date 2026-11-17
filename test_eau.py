import RPi.GPIO as GPIO
import time

# Utilisation de la numérotation BCM (GPIO 14)
pin = 18

GPIO.setmode(GPIO.BCM)
# Configuration de la broche en entrée avec une résistance de pull-down
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Test du capteur d'eau en cours (Appuyez sur Ctrl+C pour arrêter)...")

try:
    while True:
        # Lecture de l'état du capteur
        etat = GPIO.input(pin)
        
        if etat == GPIO.HIGH:
            print("💧 Présence d'eau détectée !")
        else:
            print("Sec.")
            
        time.sleep(1)

except KeyboardInterrupt:
    print("\nArrêt du test.")
finally:
    # Nettoyage des ports GPIO en quittant
    GPIO.cleanup()
