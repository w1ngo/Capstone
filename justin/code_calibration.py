#import dimentiometer_functions as dim
#import gravitometer_functions as grav
import RPi.GPIO as GPIO
#import cv2
import os.path
import json
from time import sleep
from hx711 import HX711

# Temporary file to quickly test code and replace temp values
def read_load_cell():
    GPIO.setmode(GPIO.BCM)

    tare1 = 0
    tare2 = 0
    ratio1 = 1
    ratio2 = 1


    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)  # Create hx711 object for load cell 1
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)  # Create hx711 object for load cell 2

    data1 = hx1.get_raw_data_mean(readings=30)
    data2 = hx2.get_raw_data_mean(readings=30)

    weight1 = (data1 - tare1) / ratio1  # Manual tare and unit conversion
    weight2 = (data2 - tare2) / ratio2

    GPIO.cleanup

    return weight1, weight2

    

print(read_load_cell())

#GPIO.cleanup