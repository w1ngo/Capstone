 #!/usr/bin/python3
'''
This file stores the functions needed for the dimentiometer to function properly.
    Associated functions include motor controls for the trapdoor, camera controls,
    image processing, etc.
'''

from edge_detect import detection_functions as ed
from file_io import file_io as io
import RPi.GPIO as gpio


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
        0 == 0

    elif camera == "Side":
        0 == 0

    else:
        0 == 0

    return
    #ENDOF: calibrate_camera(camera)


'''
This function performs the commands needed to open or close the trapdoor. It
    accepts one parameter, a String designating the desire to either "Open"
    or "Close" the trapdoor. It return true if no errors were encountered,
    and false otherwise.
'''
def control_trapdoor( option ):
    if option == "Open":
        0 == 0

    elif option == "Close":
        0 == 0

    else:
        0 == 0 

    return True
    #ENDOF: control_trapdoor(option)
