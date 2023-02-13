import cv2
import detection_functions as funcs
import refine_parameters   as refine
import random
from sys import platform

if __name__ == "__main__":
    
    if platform == "linux" or platform == "linux2":
        filename1 = r"./images/isolated_potato.jpg"
        filename2 = r"./images/isolated_potato2.jpg"
        filename3 = r"./images/isolated_potato3.png"

    elif platform == "win32" or platform == "win64":
        filename1 = r".\images\isolated_potato.jpg"
        filename2 = r".\images\isolated_potato2.jpg"
        filename3 = r".\images\isolated_potato3.png"

    if False:
        _, data = refine.refine( [filename1] )

    else:
        params = funcs.compile_param_list("param_refine.txt")

        height, width = funcs.find_measurements(filename1, params)
        print( f"Height: {height}, Width: {width}" )

        height, width = funcs.find_measurements(filename2, params)
        print( f"Height: {height}, Width: {width}" )

        height, width = funcs.find_measurements(filename2, params)
        print( f"Height: {height}, Width: {width}" )

