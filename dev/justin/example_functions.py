import RPi.GPIO as GPIO
import cv2
from hx711 import HX711
from time import sleep

"""
Function for opening and closing the trapdoor on the Dimentiometer.
The trapdoor is controlled by a servo motor.

Duty cycle values depend on motor.
"""
def trapdoor_control(option):
    servoPIN = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pwm = GPIO.PWM(servoPIN, 50)    # Frequency of 50 Hz
    pwm.start(0)                    # Initialize

    if option == "Open":
        pwm.ChangeDutyCycle(0)  # TEMP VALUE (0): calibrate and change to desired open position value
        sleep(0)                #TEMP VALUE (0): change to desired wait time

    elif option == "Close":
        pwm.ChangeDutyCycle(0)  # TEMP VALUE (0): calibrate and change to desired closed position value
        sleep(0)                # TEMP VALUE (0): change to desired wait time

    else:
        pwm.stop()
        GPIO.cleanup()
        return False
    
    pwm.stop()
    GPIO.cleanup()
    return True


"""
Function for controlling stepper motors on the Gravitometer.
Currently stepper 1 is vertical and stepper 2 is rotational.
    Holden TODO: clean this up
            break up into helper functions for readability
            break basket movement into two functions....lowering
            and then raising with no space to take a weight
            measurement isnt helpful
            Recomment everything
"""
def motor_control(motor):
    CW = 1
    CCW = 0
    if motor == "Vertical":
        DIR = 11
        STEP = 8
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        GPIO.output(DIR, CW)            # TEMP VALUE (CW): Change to downwards direction
        sleep(1)
        for i in range(200):            # TEMP VALUE (200): Number of steps, affects how far motor rotates
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM LOW duration
        
        sleep(10)                       # TEMP VALUE (10): Number of seconds to wait before lifting basket back up

        GPIO.output(DIR, CCW)           # TEMP VALUE (CCW): Change to upwards direction
        sleep(1)
        for i in range(200):            # TEMP VALUE (200): Number of steps, affects how far motor rotates
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM LOW duration

    elif motor == "Rotational":
        DIR = 12
        STEP = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        GPIO.output(DIR, CW)            # TEMP VALUE (CW): Change to first direction
        sleep(1)
        for i in range(200):            # TEMP VALUE (200): Number of steps, affects how far motor rotates
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM LOW duration
        
        sleep(10)                       # TEMP VALUE (10): Number of seconds to wait before lifting basket back up

        GPIO.output(DIR, CCW)           # TEMP VALUE (CCW): Change to second direction
        sleep(1)
        for i in range(200):            # TEMP VALUE (200): Number of steps, affects how far motor rotates
            GPIO.output(STEP, GPIO.HIGH)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM HIGH duration
            GPIO.output(STEP, GPIO.LOW)
            sleep(0.005)                # TEMP VALUE (0.005): Affects PWM LOW duration

    else:
        GPIO.cleanup()
        return False

    GPIO.cleanup()
    return True


"""
Function for capturing an image with the USB cameras.
"""

def take_picture(camera):
    camera_top = cv2.VideoCapture(0)  # Defines which camera is used for recording
    camera_side = cv2.VideoCapture(1)
    if camera == "Top":
        for i in range(10):
            check, frame = camera_top.read()  # starts video capture
            print(check)
            # cv2.imshow("camera1", frame1)  # shows video recording output, uncomment for testing
            cv2.waitKey(1)  # time in ms between each frame

        cv2.imwrite('top_pic.jpg', frame)
        gray_pic = cv2.imread('top_pic.jpg', cv2.IMREAD_GRAYSCALE)
        camera_top.release()
        cv2.destroyAllWindows()

    elif camera == "Side":
        for i in range(10):
            check, frame = camera_side.read()
            # cv2.imshow("camera2", frame2)
            cv2.waitKey(1)

        cv2.imwrite('side_pic.jpg', frame)
        gray_pic = cv2.imread('side_pic.jpg', cv2.IMREAD_GRAYSCALE)
        camera_side.release()
        cv2.destroyAllWindows()

    else:
        return

    return gray_pic

