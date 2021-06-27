import sys
import RPi.GPIO as GPIO
import os
import Adafruit_DHT
import urllib.request as urllib2
import smbus
import time
from ctypes import c_short
import random

DHTpin = 17 # Pour le capteur DHT11
resistorPin = 7 # Pour le capteur photoresistor
key = "1ZZREL7DJ7L2QV79" # API Key for ThingSpeak
GPIO.setmode(GPIO.BCM) # For humidity and temperature sensor
GPIO.setmode(GPIO.BOARD) # For light sensor

# Collecter les données sur la température et l'humidité du capteur DHT11
def readDHT():
	humi, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
        return humi,temp

# Collecter les données sur la lumière du Photoresistor
def readResistor():
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        diff  = time.time() - currentTime
        
    print(diff * 1000)
    time.sleep(1)
    return diff

# Méthode pour génerer des données aléatoires pour tester ThingSpeak
'''
def generateRandomData():
    temp = random.randrange(-75,75) * 0.8
    humi = random.randrange(0,100)
    light = random.randint(0,1)

    return humi, temp, light
'''

# Méthode pour envoyer les données collectées à l'API ThingSpeak
def sendData():
    print('System Ready ...')
    # URL pour envoyer les données à l'API + Ajouter la clé générée 
    URL = 'https://api.thingspeak.com/update?api_key=%s' % key
    print('Wait ...')
    while True:
        #(humi, temp, light) = generateRandomData()

        # Lire les données retournées par les fonctions
        (humi, temp) = readDHT()
        light = readResistor()

        # Ajouter les valeurs retournées à l'URL de l'API et les passer
        # en paramètres pour les envoyer à ThingSpeak
        finalURL = URL + "&field1=%s&field2=%s&field3=%s" %(temp, humi,light)
        print(finalURL)
        # Exécuter la requête avec l'URL finale générée
        s=urllib2.urlopen(finalURL)
        print(str(humi) + " " + str(temp) + " " + str(light))
        s.close()
        time.sleep(1)

def main():
    sendData()
if __name__ == '__main__':
    main()
