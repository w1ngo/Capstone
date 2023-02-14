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

    if input("Enter y to refine parameter options, or anything else to test edge detection as-is: ") == "y":
        _, data = refine.multi_refine( [filename1, filename2, filename3] )

    else:
        params = funcs.compile_param_list()
        # print(f"params compiled...{len(params)} param sets identified\n\n")

        height, width = funcs.find_measurements(filename1, params)
        print( f"Height: {height}, Width: {width}" )
        height, width = funcs.find_measurements(filename2, params)
        print( f"Height: {height}, Width: {width}" )
        height, width = funcs.find_measurements(filename3, params)
        print( f"Height: {height}, Width: {width}" )
