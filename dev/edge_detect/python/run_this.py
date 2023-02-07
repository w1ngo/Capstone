import cv2
import detection_functions as funcs
import refine_parameters   as refine
import random

if __name__ == "__main__":
    ls = []
    data = []
    
    filename1 = r"/home/wingo/work/capstone_main/dev/edge_detect/python/images/isolated_potato.jpg"
    filename2 = r"./images/isolated_potato2.jpg"
    filename3 = r"./images/isolated_potato3.png"
    
    inp = input("Enter param to perform parameters refinement, or orient to perform orientation detection testing: ")

    if inp == "param":
        _, data = refine.refine( [filename1, filename2, filename3] )

    elif inp == "orient":
        img = funcs.execute( True, True, 1, 100, False, filename1 )
        funcs.orientation( img, 1 )

        img = funcs.execute( True, True, 1, 100, False, filename2 )
        funcs.orientation( img, 1 )

        img = funcs.execute( True, True, 1, 100, False, filename3 )
        funcs.orientation( img, 1 )

    else:
        print("Unrecognized response, aborting...")

