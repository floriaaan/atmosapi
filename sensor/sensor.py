#sensor ESP8206-01 script

#acquire data from esptools?


#post data to RASPBERRY


import requests as urequests
import random
import time

"""
This script can be used to fake ESP8266 sensor
"""

def http_post(temp, humidity):
    url = 'http://192.168.43.57:5000/atmos/measure/'
    data = (temp, humidity)
    resp = urequests.post(url, data=data)

i=0
while i < 10000:
    i+=1
    temperature = random.randint(0,30)
    humidite = random.randint(0,100)
    print(type(temperature))
    print(type(humidite))
    print("we will post temperature="+str(temperature)+" and humidity="+str(humidite))
    http_post(temperature, humidite)
    time.sleep(1)