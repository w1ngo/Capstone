import RPi.GPIO as GPIO
from time import sleep
from hx711 import HX711


"""
Function for controlling stepper motors on the Gravitometer.
Stepper 1 is vertical and stepper 2 is rotational.
"""
def motor_control(motor):
    CW = 1
    CCW = 0

    # Stepper motor 1 downwards direction (clockwise)
    if motor == "Vertical Down":
        DIR = 11
        STEP = 9
        LS = 24  # Limit switch 2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(DIR, CW)
        sleep(1)

        # Exits loop when limit switch returns 0 three times in a row
        queue = [1,1,1]
        while any(queue): 
            queue.pop(0)
            queue.append(GPIO.input(LS))

            # PWM to turn motor
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.00015)
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.00005)
    
    # Stepper motor 1 upwards direction (counterclockwise)
    elif motor == "Vertical Up":
        DIR = 11
        STEP = 9
        LS = 23  # Limit switch 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(DIR, CCW)
        sleep(1)

        # Exits loop when limit switch returns 0 three times in a row
        queue = [1,1,1]
        while any(queue): 
            queue.pop(0)
            queue.append(GPIO.input(LS))

            # PWM to turn motor
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.00015)
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.00005)

    # Stepper motor 2 rotate outwards (counterclockwise)
    elif motor == "Rotational Out":
        DIR = 12
        STEP = 6
        LS = 19  # Limit switch 3
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(DIR, CCW)
        sleep(1)

        # Exits loop when limit switch returns 0 three times in a row
        queue = [1,1,1]
        while any(queue): 
            queue.pop(0)
            queue.append(GPIO.input(LS))

            # PWM to turn motor
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.003)
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.001)


    # Stepper motor 2 rotate to center (clockwise)
    elif motor == "Rotational In":
        DIR = 12
        STEP = 6
        LS = 26  # Limit switch 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.setup(LS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(DIR, CW)
        sleep(1)

        # Exits loop when limit switch returns 0 three times in a row
        queue = [1,1,1]
        while any(queue): 
            queue.pop(0)
            queue.append(GPIO.input(LS))

            # PWM to turn motor
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.003)
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.001)

    else:
        return False

    return True


"""
Function to read load cell value and calculate weight.
Returns weight of load cell 1 and 2.
"""
def read_load_cell(tare1, tare2, ratio1, ratio2):
    GPIO.setmode(GPIO.BCM)

    # Create object for both load cells
    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)
    sleep(1)

    # Get raw data output
    data1 = hx1.get_raw_data_mean(readings=30)
    data2 = hx2.get_raw_data_mean(readings=30)

    # Use tare and ratio to convert to weight in grams
    weight1 = abs(data1 - tare1) / ratio1
    weight2 = abs(data2 - tare2) / ratio2
    #print(weight1,weight2)

    return weight1, weight2

"""
Function to measure basket tare weight in air and water.
Returns tare in air and water of load cell 1 and 2.
"""
def measure_tare():
    GPIO.setmode(GPIO.BCM)

    # Create object for both load cells
    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)
    sleep(1)

    # Measure tare in air
    air_tare1 = hx1.get_raw_data_mean(readings=30)
    air_tare2 = hx2.get_raw_data_mean(readings=30)
    #print(air_tare1, air_tare2)
    motor_control("Vertical Down")
    sleep(1)

    # Measure tare in water
    water_tare1 = hx1.get_raw_data_mean(readings=30)  
    water_tare2 = hx2.get_raw_data_mean(readings=30)
    motor_control("Vertical Up")
    
    return air_tare1, air_tare2, water_tare1, water_tare2


"""
Function to measure the digital to grams conversion ratio of the load cells.
Returns the ratio of load cell 1 and 2.
"""
def measure_ratio(known_weight, tare1, tare2):
    GPIO.setmode(GPIO.BCM)

    # Create object for both load cells
    hx1 = HX711(dout_pin=14, pd_sck_pin=4, gain_channel_A=128)
    hx2 = HX711(dout_pin=15, pd_sck_pin=17, gain_channel_A=128)
    sleep(1)

    # Get raw data output
    ratio1 = hx1.get_raw_data_mean(readings=30)
    ratio2 = hx2.get_raw_data_mean(readings=30)
    #print(ratio1,ratio2)

    # Calculate load cell calibration ratio
    ratio1 = abs(ratio1 - tare1) / known_weight
    ratio2 = abs(ratio2 - tare2) / known_weight
    #print(ratio1,ratio2)

    GPIO.cleanup()
    return ratio1, ratio2
