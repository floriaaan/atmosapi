#sensor ESP8206-01 script

import urequests
import random
import time

import si7021
import machine
i2C = machine.I2C(-1, machine.Pin(2), machine.Pin(0))
temp_sensor = si7021.Si7021(i2C)

"""
This script can be used to fake ESP8266 sensor
"""

def http_post(probe_id, temp, humidity):
    url = 'http://192.168.43.57:5000/atmos/measure/add/'+ str(probe_id) +'/' + str(temp) + '+' + str(humidity) 
    resp = urequests.post(url)

def moyenneTemp():
    var1 = temp_sensor.temperature
    time.sleep(1)
    var2 = temp_sensor.temperature
    time.sleep(1)
    var3 = temp_sensor.temperature
    time.sleep(1)
    var4 = temp_sensor.temperature
    time.sleep(1)
    var5 = temp_sensor.temperature
    time.sleep(1)
    return (var1 + var2 + var3 + var4 + var5) / 5

def moyenneHumid():
    var1 = temp_sensor.relative_humidity
    time.sleep(1)
    var2 = temp_sensor.relative_humidity
    time.sleep(1)
    var3 = temp_sensor.relative_humidity
    time.sleep(1)
    var4 = temp_sensor.relative_humidity
    time.sleep(1)
    var5 = temp_sensor.relative_humidity
    time.sleep(1)
    return (var1 + var2 + var3 + var4 + var5) / 5


while True:

    http_post(1, moyenneTemp(), moyenneHumid())
    time.sleep(1)