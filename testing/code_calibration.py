#import dimentiometer_functions as dim
#import gravitometer_functions as grav
import RPi.GPIO as GPIO
#import cv2
import os.path
import json
from time import sleep
#from hx711_multi import HX711
from hx711 import HX711
from time import perf_counter

# Temporary file to quickly test code and replace temp values
def read_load_cell():
    GPIO.setmode(GPIO.BCM)
    
    hx1 = HX711(dout_pin=14, pd_sck_pin=4)
    hx2 = HX711(dout_pin=15, pd_sck_pin=17)

    result1 = hx1.zero(readings=30)
    result2 = hx2.zero(readings=30)
    while True:
        known_weight = float(input("enter value:"))
        data1 = abs(hx1.get_data_mean(readings=30))
        data2 = abs(hx2.get_data_mean(readings=30))
   
        #known1 = float(data1 / (data1+data2)) * known_weight
        #known2 = float(data2 / (data1+data2)) * known_weight

        ratio1 = data1/known_weight
        ratio2 = data2/known_weight
    
        hx1.set_scale_ratio(ratio1)
        hx2.set_scale_ratio(ratio2)
        for i in range(10):
            #weight1 = abs(hx1.get_weight_mean(20))
            weight2 = abs(hx2.get_weight_mean(20))
            print(weight2)

if __name__ == "__main__":
    read_load_cell()


