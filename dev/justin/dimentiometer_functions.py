import RPi.GPIO as GPIO
import cv2
from time import sleep


"""
Function for capturing an image with the USB cameras.
"""

def take_picture(camera):
    IR = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("Waiting for potato...")
    while not GPIO.input(IR):  # Wait for IR sensor
        continue
    print("Potato detected!")
    camera_top = cv2.VideoCapture(0)  # Defines which camera is used for recording
    camera_side = cv2.VideoCapture(1)
    if camera == "Top":
        for i in range(10):
            check, frame = camera_top.read()  # starts video capture
            # cv2.imshow("camera_top", frame)  # shows video recording output, uncomment for testing
            cv2.waitKey(1)  # time in ms between each frame

        cv2.imwrite('top_pic.jpg', frame)
        gray_pic = cv2.imread('top_pic.jpg', cv2.IMREAD_GRAYSCALE)
        camera_top.release()
        cv2.destroyAllWindows()

    elif camera == "Side":
        for i in range(10):
            check, frame = camera_side.read()
            # cv2.imshow("camera_side", frame)
            cv2.waitKey(1)

        cv2.imwrite('side_pic.jpg', frame)
        gray_pic = cv2.imread('side_pic.jpg', cv2.IMREAD_GRAYSCALE)
        camera_side.release()
        cv2.destroyAllWindows()

    else:
        return

    return gray_pic  # Currently returns 2D list


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
    pwm.start(0)  # Initialize

    if option == "Open":
        pwm.ChangeDutyCycle(0)  # TEMP VALUE (0): calibrate and change to desired open position value
        sleep(0)    #TEMP VALUE (0): change to desired wait time

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
