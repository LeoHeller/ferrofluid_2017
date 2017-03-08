import os
from os import sys, path
sys.path.append("/home/pi/py/")

import gpio
import wiringpi
import time


gpio.setup()
gpio.mag_st(0, 100)
time.sleep(10)
gpio.mag_st(0,0)


