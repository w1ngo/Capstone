import RPi.GPIO as GPIO
from hx711 import HX711

"""
Example code to hx711 and load cell. Refer to https://pinout.xyz/
for GPIO pin locations, as they differ from the physical pin location.
"""


GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
hx = HX711(dout_pin=21, pd_sck_pin=20)  # create an object
print(hx.get_raw_data_mean())  # get raw data reading from hx711
GPIO.cleanup()
