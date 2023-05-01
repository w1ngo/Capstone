import RPi.GPIO as GPIO
from time import sleep
from hx711 import HX711


"""
Function for controlling stepper motors on the Gravitometer.
Currently stepper 1 is vertical and stepper 2 is rotational.
"""
def motor_control(motor):
    CW = 1
    CCW = 0
    if motor == "Vertical Down":
        DIR = 11
        STEP = 8
        LS = 23  # Limit switch 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(DIR, CW)    # TEMP VALUE (CW): Change to downwards direction
        sleep(1)
        # for i in range(200):    # TEMP VALUE (200): Number of steps, affects how far motor rotates
        while GPIO.input(LS):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)  # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005) # TEMP VALUE (0.005): Affects PWM LOW duration

            # if GPIO.input(0):  # TEMP VALUE (0): Limit switch 1
            #    break
    
    
    elif motor == "Vertical Up":
        DIR = 11
        STEP = 8
        LS = 7  # Limit switch 2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(DIR, CCW)    # TEMP VALUE (CCW): Change to upwards direction
        sleep(1)
        # for i in range(200):    # TEMP VALUE (200): Number of steps, affects how far motor rotates
        while GPIO.input(LS):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)  # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005) # TEMP VALUE (0.005): Affects PWM LOW duration

            # if GPIO.input(0):  # TEMP VALUE (0): Limit switch 2
            #    break

    
    elif motor == "Rotational Out":
        DIR = 12
        STEP = 13
        LS = 19  # Limit switch 3
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(DIR, CW)    # TEMP VALUE (CW): Change to first direction
        sleep(1)
        # for i in range(200):    # TEMP VALUE (200): Number of steps, affects how far motor rotates
        while GPIO.input(LS):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)  # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005) # TEMP VALUE (0.005): Affects PWM LOW duration
            
            # if GPIO.input(0):  # TEMP VALUE (0): Limit switch 3
            #    break

        sleep(10)   # TEMP VALUE (10): Number of seconds to wait before lifting basket back up

    
    elif motor == "Rotational In":
        DIR = 12
        STEP = 13
        LS = 26  # Limit switch 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.output(DIR, CCW)    # TEMP VALUE (CCW): Change to second direction
        sleep(1)
        # for i in range(200):    # TEMP VALUE (200): Number of steps, affects how far motor rotates
        while GPIO.input(LS):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)  # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005) # TEMP VALUE (0.005): Affects PWM LOW duration
            
            # if GPIO.input(0):  # TEMP VALUE (0): Limit switch 4
            #    break
    else:
        GPIO.cleanup()
        return False

    GPIO.cleanup()
    return True


"""
Function to read load cell value. 
"""
def read_load_cell(tare1, tare2, ratio1, ratio2):
    GPIO.setmode(GPIO.BCM)

    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)  # Create hx711 object for load cell 1
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)  # Create hx711 object for load cell 2

    data1 = hx1.get_raw_data_mean(readings=30)
    data2 = hx2.get_raw_data_mean(readings=30)

    weight1 = (data1 - tare1) / ratio1  # Manual tare and unit conversion
    weight2 = (data2 - tare2) / ratio2

    return weight1, weight2


def measure_tare():
    GPIO.setmode(GPIO.BCM)

    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)  # Create hx711 object for load cell 1
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)  # Create hx711 object for load cell 2

    air_tare1 = hx1.get_raw_data_mean(readings=30)  # Measure tare in air
    air_tare2 = hx2.get_raw_data_mean(readings=30)

    motor_control("Vertical Down")

    water_tare1 = hx1.get_raw_data_mean(readings=30)  # Measure tare in water
    water_tare2 = hx2.get_raw_data_mean(readings=30)

    motor_control("Vertical Up")
    
    return air_tare1, air_tare2, water_tare1, water_tare2


def measure_ratio(known_weight, tare1, tare2):
    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)  # Create hx711 object for load cell 1
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)  # Create hx711 object for load cell 2
    
    ratio1 = hx1.get_raw_data_mean(readings=30)
    ratio2 = hx2.get_raw_data_mean(readings=30)

    ratio1 = (ratio1 - tare1) / known_weight
    ratio2 = (ratio2 - tare2) / known_weight

    return ratio1, ratio2

