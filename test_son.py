import RPi.GPIO as GPIO
import time

# Utilisation de la broche GPIO 14
pin = 23

GPIO.setmode(GPIO.BCM)
# Configuration de la broche en entrée
GPIO.setup(pin, GPIO.IN)

print("Test du capteur de son en cours (Appuyez sur Ctrl+C pour arrêter)...")
print("Tapez dans vos mains ou parlez fort !")

# Fonction exécutée automatiquement à chaque détection de son
def alerte_son(channel):
    print("🔊 Bruit détecté !")

# Surveillance de la broche en arrière-plan
# Le paramètre 'bouncetime=300' (en millisecondes) empêche le capteur de 
# déclencher plusieurs alertes pour un seul et même bruit continu.
GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(pin, alerte_son)

try:
    # La boucle principale tourne dans le vide, les interruptions font le travail
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nArrêt du test.")
finally:
    # Nettoyage des ports GPIO avant de quitter
    GPIO.cleanup()
