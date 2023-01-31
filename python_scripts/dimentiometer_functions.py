#!/usr/bin/python3

'''
This file stores the functions needed for the dimentiometer to function properly.
    Associated functions include motor controls for the trapdoor, camera controls,
    image processing, etc.
'''

import RPI.GPIO as gpio
import computer_vision_functions as cviz


'''
This function performs the steps necessary to calibrate the camera according
    to the specific setup expected for dimentiometer operation. It is designed
    to occur relatively quickly to allow for regular re-calibration of the camera
    during operation to retain good accuracy and prevent drift. It accepts one 
    parameter, which indicates whether the "Top" camera or the "Side" camera is to
    be calibrated. As the calibration refers to parameters that need to be 
    applied to camera inputs, the return value is a tuple of said data
'''
def calibrate_camera( camera ):
    if camera == "Top":


    elif camera == "Side":


    else:


    return
    #ENDOF: calibrate_camera(camera)


'''
This function takes a picture remotely using the connection to the camera. It
    only takes one picture from one camera, so it accepts one input, namely the
    designation of "Top" camera or "Side" camera. It returns a 2-D array of tuples.
    The tuples represent the RGB intensities of each pixel, and element 0-0 represents
    the pixel in the top-left corner of the image (relative to the perspective of someone
    looking through the camera lens upon the surface photographed).
'''
def take_picture( camera ):
    if camera == "Top":


    elif camera == "Bottom":


    else:


    return
    #ENDOF: take_picture(camera)


'''

'''
def measure_potato():
    
    return
    #ENDOF: measure_potato()


'''

'''
def record_data():
    
    return
    #ENDOF: record_data()


'''
This function performs the commands needed to open or close the trapdoor. It
    accepts one parameter, a String designating the desire to either "Open"
    or "Close" the trapdoor. It return true if no errors were encountered,
    and false otherwise.
'''
def control_trapdoor( option ):
    if option == "Open":


    elif option == "Close":


    else:
        

    return True
    #ENDOF: control_trapdoor(option)


