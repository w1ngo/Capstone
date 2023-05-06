import RPi.GPIO as GPIO
import cv2
from time import sleep

'''
Function for opening and closing the trapdoor on the Dimentiometer.
The trapdoor is controlled by a servo motor.

Duty cycle values depend on motor.
'''
def trapdoor_control(option):
    servoPIN = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pwm = GPIO.PWM(servoPIN, 50)    # Frequency of 50 Hz
    pwm.start(0)  # Initialize

    # Open trapdoor
    if option == "Open":
        pwm.ChangeDutyCycle(0)  # TEMP VALUE (0): calibrate and change to desired open position value
        sleep(0)    #TEMP VALUE (0): change to desired wait time

    # Close trapdoor
    elif option == "Close":
        pwm.ChangeDutyCycle(0)  # TEMP VALUE (0): calibrate and change to desired closed position value
        sleep(0)    #TEMP VALUE (0): change to desired wait time

    else:
        pwm.stop()
        GPIO.cleanup()
        return False
    
    pwm.stop()
    GPIO.cleanup()
    return True
