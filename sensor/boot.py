# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import Sensor
#import webrepl
#webrepl.start()
gc.collect()

print('\n')

from Network_config import connect_Tetra
connect_Tetra()

from Sensor import sensor_dispsend , sensor_disp

print('\n')

