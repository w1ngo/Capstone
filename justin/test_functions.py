import dimentiometer_functions as dim
import gravitometer_functions as grav
import RPi.GPIO as GPIO
import cv2
import os.path
import json
from time import sleep
from hx711 import HX711


def test_camera_picture():
    while True:
        print("1) Top camera\n"
              "2) Side camera\n"
              "3) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            camera = cv2.VideoCapture(0)
        elif option == "2":
            camera = cv2.VideoCapture(1)
        else:
            break
        print("Press q to quit.")
        while True:
            check, frame = camera.read()  # starts video capture
            cv2.imshow("camera", frame)  # shows video recording output, uncomment for testing
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.imwrite('test_pic.jpg', frame)
        gray_pic = cv2.imread('test_pic.jpg', cv2.IMREAD_GRAYSCALE)
        print(gray_pic)
        camera.release()
        cv2.destroyAllWindows()
    

def test_ir_sensor():
    while True:
        print("1) Test IR Sensor\n"
              "2) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            IR = 22
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(IR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print("IR: ", GPIO.input(IR), "\n")
            GPIO.cleanup()
        else:
            break


def test_servo_motor():
    while True:
        print("1) Open\n"
              "2) Close\n"
              "3) Choose position manually\n"
              "4) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            dim.trapdoor_control("Open")
        elif option == "2":
            dim.trapdoor_control("Close")
        elif option == "3":
            num = input("Enter value: ").strip()  # might need to limit this to certain range, or remove it altogether
            if num.isnumeric():
                int(num)
            else:
                continue
            servoPIN = 27
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servoPIN, GPIO.OUT)
            pwm = GPIO.PWM(servoPIN, 50)    # Frequency of 50 Hz
            pwm.start(0)  # Initialize
            pwm.ChangeDutyCycle(num)
            sleep(0)    #TEMP VALUE (0): change to desired wait time
            pwm.stop()
            GPIO.cleanup()
        else:
            dim.trapdoor_control("Close")
            break
    

def test_load_cell():
    GPIO.setmode(GPIO.BCM)
    while True:
        print("1) Raw output\n"
              "2) Final weight\n"
              "3) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            hx1 = HX711(dout_pin=14, pd_sck_pin=4)  # Create hx711 object for load cell 1
            hx2 = HX711(dout_pin=15, pd_sck_pin=17)  # Create hx711 object for load cell 2
            print("LC1: ", hx1.get_raw_data_mean(readings=30), "\nLC2: ", hx2.get_raw_data_mean(readings=30), "\n")
        elif option == "2":
            if os.path.isfile('tare.json') and os.path.getsize('tare.json') > 0 and os.path.isfile('ratio.json') and os.path.getsize('ratio.json') > 0:
                with open('tare.json', 'r') as file:
                    tare_dict = json.load(file)
                with open('ratio.json', 'r') as file:
                    ratio_dict = json.load(file)
                air_weight1, air_weight2 = grav.read_load_cell(tare_dict['Air1'], tare_dict['Air2'], ratio_dict['Ratio1'], ratio_dict['Ratio2'])
                print("LC1:", air_weight1, "\nLC2: ", air_weight2, "\n")
        else:
            break
    GPIO.cleanup()


def test_stepper_motor():
    while True:
        print("1) Move Down\n"
              "2) Move Up\n"
              "3) Rotate out\n"
              "4) Rotate in\n"
              "5) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            grav.motor_control("Vertical Down")
        elif option == "2":
            grav.motor_control("Vertical Up")
        elif option == "3":
            #grav.motor_control("Vertical Up")
            grav.motor_control("Rotational Out")
        elif option == "4":
            #grav.motor_control("Vertical Up")
            grav.motor_control("Rotational In")
        else:
            #grav.motor_control("Vertical Up")
            #grav.motor_control("Rotational In")
            break


def test_limit_switch():
    while True:
        print("1) Test limit switches\n"
            "2) Return to main screen\n")
        option = input("Select an option: ").strip()
        if option == "1":
            LS1 = 24    # Down
            LS2 = 23     # Up
            LS3 = 19    # Out
            LS4 = 26   # In
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LS1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(LS2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(LS3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(LS4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            while True:

                print("LS2 (Down): ", GPIO.input(LS1), "\nLS1 (Up): ", GPIO.input(LS2), "\nLS3 (Out): ", GPIO.input(LS3), "\nLS4 (In): ", GPIO.input(LS4), "\n")
                sleep(1)
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(7, GPIO.OUT)
            while True:
                GPIO.output(7, GPIO.HIGH)
            
