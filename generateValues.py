#sensor ESP8206-01 script

import requests
import random
import time
import json



def http_post(probe_id, temp, humidity):
    url = 'http://localhost:5000/atmos/measure/add/'
    data = {
        'probe_id' : probe_id,
        'temp' : temp,
        'humidity' : humidity
    }
    headers = {
        'charset': 'utf-8'
    }
    resp = requests.post(url, json=data, headers=headers)

while True:
    try:
        temp = random.randint(17, 23)
        humid = random.randint(50, 60)
        probe = random.randint(1,12)
        http_post(probe, temp, humid)
        print("POST: Sonde:"+ str(probe) + " + Temp :" + str(temp) + ' + Humid : ' + str(humid))
        #time.sleep(1)
    except KeyboardInterrupt:
        exit()
    except:
        print("!!!ERROR!!!")