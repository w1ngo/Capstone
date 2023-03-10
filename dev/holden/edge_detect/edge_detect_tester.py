import cv2
import detection_functions as funcs
import refine_parameters   as refine
import random
from sys import platform

if __name__ == "__main__":
    
    if platform == "linux" or platform == "linux2":
        filenames = [ r"./images/isolated_potato.jpg",  \
                      r"./images/isolated_potato2.jpg", \
                      r"./images/isolated_potato3.png", \
                      r"./images/IMG_4011.jpg",         \
                      r"./images/IMG_4012.jpg",         \
                      r"./images/IMG_4013.jpg" ]

    elif platform == "win32" or platform == "win64":
        filenames = [ r".\images\isolated_potato.jpg",  \
                      r".\images\isolated_potato2.jpg", \
                      r".\images\isolated_potato3.png", \
                      r".\images\IMG_4011.jpg",         \
                      r".\images\IMG_4012.jpg",         \
                      r".\images\IMG_4013.jpg" ]

    if input("Enter r to refine parameter options or t test edge detection as-is: ") in ("R", "r"):
        _, data = refine.multi_refine( [filename1, filename2, filename3] )

    else:
        disp = input("Display bounding boxes [Y/n]? ") in ("Y", "y")
        params = funcs.compile_param_list()
        [print(f"Potato at <{filenames[i]:<29}> pixel dims: {elem[0]:<18} x {elem[1]:<18}") \
         for i, elem in enumerate( list(map(lambda file : funcs.find_measurements(file, params, disp), filenames)) )  \
         if elem[0] != 0]
