import RPi.GPIO as GPIO
from time import sleep

"""
Example code for stepper motor testing. Direction and speed of the motors
are being tested. Should work with Nema motors, such as 17 and 23.

1 Microstep setting (ON, ON, OFF) results in 200 steps for a full roation.
"""

# Set pins for DIR and STEP
DIR = 10
STEP = 8

CW = 1
CCW = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.output(DIR, CW)  # test CW rotation 
sleep(1.0)  # allows motor time to switch direction

# Create loop for PWM
for i in range(200):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(0.005)  # Affects PWM HIGH duration
    GPIO.output(STEP, GPIO.LOW)
    sleep(0.005) # Affects PWM LOW duration

GPIO.output(DIR, CCW)  # test CCW rotation 
sleep(1.0)  # allows motor time to switch direction

# Create loop for PWM
for i in range(200):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(0.007)  # Affects PWM HIGH duration
    GPIO.output(STEP, GPIO.LOW)
    sleep(0.003) # Affects PWM LOW duration

GPIO.cleanup()